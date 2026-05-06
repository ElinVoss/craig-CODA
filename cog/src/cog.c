/*
 * cog.c — Field Computation Executor
 *
 * There are no instructions. There are only responses.
 *
 * Build:  gcc -O2 -o cog cog.c -lm
 * Run:    ./cog model/
 */

#include "cog.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <ctype.h>
#include <dirent.h>

/* ═══════════════════════════════════════════════════════════════════════════
 * LEXER
 * ═══════════════════════════════════════════════════════════════════════════ */

typedef enum {
    TOK_WORD, TOK_STRING, TOK_NUMBER,
    TOK_LBRACE, TOK_RBRACE,
    TOK_LBRACKET, TOK_RBRACKET,
    TOK_COLON, TOK_COMMA, TOK_ARROW,
    TOK_EOF, TOK_ERROR
} TokType;

typedef struct {
    TokType type;
    char    val[256];
    float   num;
} Token;

typedef struct {
    const char *src;
    int         pos;
    int         line;
    char        file[256];
} Lexer;

static void lex_init(Lexer *l, const char *src, const char *file) {
    l->src  = src;
    l->pos  = 0;
    l->line = 1;
    strncpy(l->file, file, 255);
}

static char lex_peek(Lexer *l) { return l->src[l->pos]; }
static char lex_next(Lexer *l) {
    char c = l->src[l->pos++];
    if (c == '\n') l->line++;
    return c;
}

static void lex_skip_ws_comment(Lexer *l) {
    while (1) {
        char c = lex_peek(l);
        if (c == '\0') return;
        if (isspace((unsigned char)c)) { lex_next(l); continue; }
        if (c == '#') {
            while (lex_peek(l) && lex_peek(l) != '\n') lex_next(l);
            continue;
        }
        break;
    }
}

static Token lex_token(Lexer *l) {
    Token t = {0};
    lex_skip_ws_comment(l);
    char c = lex_peek(l);

    if (c == '\0') { t.type = TOK_EOF; return t; }

    if (c == '{') { lex_next(l); t.type = TOK_LBRACE;   return t; }
    if (c == '}') { lex_next(l); t.type = TOK_RBRACE;   return t; }
    if (c == '[') { lex_next(l); t.type = TOK_LBRACKET; return t; }
    if (c == ']') { lex_next(l); t.type = TOK_RBRACKET; return t; }
    if (c == ':') { lex_next(l); t.type = TOK_COLON;    return t; }
    if (c == ',') { lex_next(l); t.type = TOK_COMMA;    return t; }

    /* Arrow -> */
    if (c == '-' && l->src[l->pos+1] == '>') {
        lex_next(l); lex_next(l);
        t.type = TOK_ARROW; return t;
    }

    /* String */
    if (c == '"') {
        lex_next(l);
        int i = 0;
        while (lex_peek(l) && lex_peek(l) != '"') {
            if (i < 254) t.val[i++] = lex_next(l);
            else lex_next(l);
        }
        if (lex_peek(l) == '"') lex_next(l);
        t.val[i] = '\0';
        t.type = TOK_STRING;
        return t;
    }

    /* Number (may be negative) */
    if (isdigit((unsigned char)c) || (c == '-' && isdigit((unsigned char)l->src[l->pos+1]))) {
        int i = 0;
        if (c == '-') t.val[i++] = lex_next(l);
        while (isdigit((unsigned char)lex_peek(l)) || lex_peek(l) == '.') {
            if (i < 254) t.val[i++] = lex_next(l);
            else lex_next(l);
        }
        t.val[i] = '\0';
        t.num  = (float)atof(t.val);
        t.type = TOK_NUMBER;
        return t;
    }

    /* Word (identifier, keyword) */
    if (isalpha((unsigned char)c) || c == '_') {
        int i = 0;
        while (isalnum((unsigned char)lex_peek(l)) || lex_peek(l) == '_' || lex_peek(l) == '.') {
            if (i < 254) t.val[i++] = lex_next(l);
            else lex_next(l);
        }
        t.val[i] = '\0';
        t.type = TOK_WORD;
        return t;
    }

    fprintf(stderr, "[cog] unknown char '%c' at %s:%d\n", c, l->file, l->line);
    lex_next(l);
    t.type = TOK_ERROR;
    return t;
}

/* Lookahead-1 lexer */
typedef struct {
    Lexer   lex;
    Token   ahead;
    int     has_ahead;
} Parser;

static void parser_init(Parser *p, const char *src, const char *file) {
    lex_init(&p->lex, src, file);
    p->has_ahead = 0;
}

static Token parser_peek(Parser *p) {
    if (!p->has_ahead) {
        p->ahead     = lex_token(&p->lex);
        p->has_ahead = 1;
    }
    return p->ahead;
}

static Token parser_consume(Parser *p) {
    Token t = parser_peek(p);
    p->has_ahead = 0;
    return t;
}

static int parser_expect(Parser *p, TokType type, const char *ctx) {
    Token t = parser_consume(p);
    if (t.type != type) {
        fprintf(stderr, "[cog] expected token %d in %s, got %d ('%s')\n",
                type, ctx, t.type, t.val);
        return 0;
    }
    return 1;
}

/* ═══════════════════════════════════════════════════════════════════════════
 * UTILITIES
 * ═══════════════════════════════════════════════════════════════════════════ */

Trust trust_from_string(const char *s) {
    if (strcmp(s, "stable_core")        == 0) return TRUST_STABLE_CORE;
    if (strcmp(s, "project_constraint") == 0) return TRUST_PROJECT_CONSTRAINT;
    if (strcmp(s, "episodic")           == 0) return TRUST_EPISODIC;
    if (strcmp(s, "prose_voice")        == 0) return TRUST_PROSE_VOICE;
    if (strcmp(s, "interpretive")       == 0) return TRUST_INTERPRETIVE;
    if (strcmp(s, "review_only")        == 0) return TRUST_REVIEW_ONLY;
    return TRUST_EPISODIC;
}

const char *trust_to_string(Trust t) {
    switch (t) {
        case TRUST_STABLE_CORE:        return "stable_core";
        case TRUST_PROJECT_CONSTRAINT: return "project_constraint";
        case TRUST_EPISODIC:           return "episodic";
        case TRUST_PROSE_VOICE:        return "prose_voice";
        case TRUST_INTERPRETIVE:       return "interpretive";
        case TRUST_REVIEW_ONLY:        return "review_only";
        default:                       return "unknown";
    }
}

int cell_find(Field *f, const char *label) {
    for (int i = 0; i < f->cell_count; i++) {
        if (strcmp(f->cells[i].label, label) == 0) return i;
    }
    return -1;
}

static int cell_alloc(Field *f, const char *label) {
    if (f->cell_count >= MAX_CELLS) {
        fprintf(stderr, "[cog] MAX_CELLS reached\n");
        return -1;
    }
    int idx = f->cell_count++;
    Cell *c = &f->cells[idx];
    memset(c, 0, sizeof(Cell));
    strncpy(c->label, label, MAX_LABEL - 1);
    c->threshold        = 1.0f;
    c->potential        = 0.0f;
    c->resting          = 0.0f;
    c->decay            = 0.9f;
    c->confidence       = 0.8f;
    c->refractory_period= 3;
    c->state            = STATE_RESTING;
    c->interrupt_id     = -1;
    c->is_output        = 0;
    c->output_priority  = 999;
    c->activation_count = 0;
    return idx;
}

/* ═══════════════════════════════════════════════════════════════════════════
 * PARSER — .cog file format
 *
 * cell "label" {
 *   trust: stable_core
 *   threshold: 1.2
 *   decay: 0.85
 *   confidence: 0.9
 *   refractory: 4
 *   tags: [identity, core]
 *   summary: "text"
 *   output: true
 *   output_priority: 1
 *   interrupt: contradicts_fired
 * }
 *
 * channel {
 *   from: "label_a"
 *   to:   "label_b"
 *   weight: 0.7
 *   polarity: excitatory
 *   type: direct
 *   delay: 0
 * }
 * ═══════════════════════════════════════════════════════════════════════════ */

static void parse_tags(Parser *p, Cell *c) {
    /* consume '[' already done by caller */
    while (1) {
        Token t = parser_peek(p);
        if (t.type == TOK_RBRACKET || t.type == TOK_EOF) break;
        if (t.type == TOK_WORD || t.type == TOK_STRING) {
            parser_consume(p);
            if (c->tag_count < MAX_TAGS) {
                strncpy(c->tags[c->tag_count++], t.val, MAX_TAG_LEN - 1);
            }
        }
        t = parser_peek(p);
        if (t.type == TOK_COMMA) parser_consume(p);
    }
    parser_expect(p, TOK_RBRACKET, "tags");
}

static int parse_cell(Parser *p, Field *f) {
    /* consume cell keyword already done */
    Token name_tok = parser_consume(p);
    if (name_tok.type != TOK_STRING && name_tok.type != TOK_WORD) {
        fprintf(stderr, "[cog] cell expects a name string\n");
        return 0;
    }

    int idx = cell_find(f, name_tok.val);
    if (idx < 0) idx = cell_alloc(f, name_tok.val);
    if (idx < 0) return 0;
    Cell *c = &f->cells[idx];

    if (!parser_expect(p, TOK_LBRACE, "cell body")) return 0;

    while (1) {
        Token t = parser_peek(p);
        if (t.type == TOK_RBRACE || t.type == TOK_EOF) break;
        if (t.type != TOK_WORD) { parser_consume(p); continue; }
        parser_consume(p);

        if (!parser_expect(p, TOK_COLON, t.val)) return 0;
        Token val = parser_consume(p);

        if (strcmp(t.val, "trust") == 0) {
            c->trust = trust_from_string(val.val);
        } else if (strcmp(t.val, "threshold") == 0) {
            c->threshold = val.num;
        } else if (strcmp(t.val, "decay") == 0) {
            c->decay = val.num;
        } else if (strcmp(t.val, "confidence") == 0) {
            c->confidence = val.num;
        } else if (strcmp(t.val, "refractory") == 0) {
            c->refractory_period = (int)val.num;
        } else if (strcmp(t.val, "resting") == 0) {
            c->resting = val.num;
        } else if (strcmp(t.val, "voice_score") == 0) {
            c->voice_score = val.num;
        } else if (strcmp(t.val, "summary") == 0) {
            strncpy(c->summary, val.val, 255);
        } else if (strcmp(t.val, "output") == 0) {
            c->is_output = (strcmp(val.val, "true") == 0) ? 1 : 0;
        } else if (strcmp(t.val, "output_priority") == 0) {
            c->output_priority = (int)val.num;
        } else if (strcmp(t.val, "interrupt") == 0) {
            if (strcmp(val.val, "contradicts_fired")      == 0) c->interrupt_id = INT_CONTRADICTS_FIRED;
            else if (strcmp(val.val, "review_only_approached") == 0) c->interrupt_id = INT_REVIEW_ONLY_APPROACHED;
            else if (strcmp(val.val, "energy_depleted")   == 0) c->interrupt_id = INT_ENERGY_DEPLETED;
            else if (strcmp(val.val, "trust_floor_violated") == 0) c->interrupt_id = INT_TRUST_FLOOR_VIOLATED;
            else if (strcmp(val.val, "crystallize_threshold") == 0) c->interrupt_id = INT_CRYSTALLIZE_THRESHOLD;
        } else if (strcmp(t.val, "tags") == 0) {
            /* val was '[' but we consumed it — re-check */
            /* parser consumed one token as val; if it's LBRACKET parse tags */
            if (val.type == TOK_LBRACKET) {
                parse_tags(p, c);
            }
        }
    }
    parser_expect(p, TOK_RBRACE, "cell end");
    return 1;
}

static int parse_channel(Parser *p, Field *f) {
    if (!parser_expect(p, TOK_LBRACE, "channel body")) return 0;

    char from_label[MAX_LABEL] = {0};
    char to_label[MAX_LABEL]   = {0};
    float weight    = 0.5f;
    Polarity pol    = CHAN_EXCITATORY;
    ChanType type   = CHAN_DIRECT;
    int delay       = 0;

    while (1) {
        Token t = parser_peek(p);
        if (t.type == TOK_RBRACE || t.type == TOK_EOF) break;
        if (t.type != TOK_WORD) { parser_consume(p); continue; }
        parser_consume(p);
        if (!parser_expect(p, TOK_COLON, t.val)) return 0;
        Token val = parser_consume(p);

        if (strcmp(t.val, "from") == 0) {
            strncpy(from_label, val.val, MAX_LABEL - 1);
        } else if (strcmp(t.val, "to") == 0) {
            strncpy(to_label, val.val, MAX_LABEL - 1);
        } else if (strcmp(t.val, "weight") == 0) {
            weight = val.num;
        } else if (strcmp(t.val, "polarity") == 0) {
            pol = (strcmp(val.val, "inhibitory") == 0) ? CHAN_INHIBITORY : CHAN_EXCITATORY;
        } else if (strcmp(t.val, "type") == 0) {
            if (strcmp(val.val, "delayed")    == 0) type = CHAN_DELAYED;
            else if (strcmp(val.val, "stochastic") == 0) type = CHAN_STOCHASTIC;
        } else if (strcmp(t.val, "delay") == 0) {
            delay = (int)val.num;
        }
    }
    parser_expect(p, TOK_RBRACE, "channel end");

    /* Resolve labels to indices (cells must be loaded first) */
    int from_idx = cell_find(f, from_label);
    int to_idx   = cell_find(f, to_label);
    if (from_idx < 0 || to_idx < 0) {
        /* Deferred — cells may not be loaded yet; store by label? */
        /* For simplicity: skip unresolved channels. Load cells before channels. */
        return 1;
    }

    if (f->channel_count >= MAX_CHANNELS) {
        fprintf(stderr, "[cog] MAX_CHANNELS reached\n");
        return 0;
    }
    Channel *ch = &f->channels[f->channel_count++];
    ch->from_idx = from_idx;
    ch->to_idx   = to_idx;
    ch->weight   = weight;
    ch->polarity = pol;
    ch->type     = type;
    ch->delay    = delay;
    ch->active   = 1;
    return 1;
}

static int parse_cog(Parser *p, Field *f) {
    while (1) {
        Token t = parser_peek(p);
        if (t.type == TOK_EOF) break;
        if (t.type == TOK_ERROR) { parser_consume(p); continue; }
        if (t.type != TOK_WORD) { parser_consume(p); continue; }
        parser_consume(p);

        if (strcmp(t.val, "cell") == 0) {
            parse_cell(p, f);
        } else if (strcmp(t.val, "channel") == 0) {
            parse_channel(p, f);
        }
        /* other top-level keywords (future: group, bios, field_config) */
    }
    return 1;
}

/* ─── File loading ─────────────────────────────────────────────────────── */

static char *read_file(const char *path) {
    FILE *fp = fopen(path, "rb");
    if (!fp) return NULL;
    fseek(fp, 0, SEEK_END);
    long size = ftell(fp);
    rewind(fp);
    char *buf = malloc(size + 1);
    if (!buf) { fclose(fp); return NULL; }
    fread(buf, 1, size, fp);
    buf[size] = '\0';
    fclose(fp);
    return buf;
}

int cog_load_file(Field *f, const char *path) {
    char *src = read_file(path);
    if (!src) {
        fprintf(stderr, "[cog] cannot read: %s\n", path);
        return 0;
    }
    Parser p;
    parser_init(&p, src, path);
    int ok = parse_cog(&p, f);
    free(src);
    return ok;
}

int cog_load_dir(Field *f, const char *dir_path) {
    DIR *d = opendir(dir_path);
    if (!d) {
        fprintf(stderr, "[cog] cannot open dir: %s\n", dir_path);
        return 0;
    }
    struct dirent *entry;
    char path[512];
    int loaded = 0;
    while ((entry = readdir(d))) {
        size_t len = strlen(entry->d_name);
        if (len < 5) continue;
        if (strcmp(entry->d_name + len - 4, ".cog") != 0) continue;
        snprintf(path, sizeof(path), "%s/%s", dir_path, entry->d_name);
        if (cog_load_file(f, path)) loaded++;
    }
    closedir(d);
    return loaded;
}

/* ═══════════════════════════════════════════════════════════════════════════
 * BIOS — Power-On Self-Test + Boot
 * ═══════════════════════════════════════════════════════════════════════════ */

int bios_post(Field *f) {
    int ok = 1;

    /* POST-1: every cell must have a label */
    for (int i = 0; i < f->cell_count; i++) {
        if (f->cells[i].label[0] == '\0') {
            fprintf(stderr, "[POST] FAIL: cell %d has no label\n", i);
            ok = 0;
        }
    }

    /* POST-2: no channel references out-of-range cell */
    for (int i = 0; i < f->channel_count; i++) {
        Channel *ch = &f->channels[i];
        if (ch->from_idx < 0 || ch->from_idx >= f->cell_count ||
            ch->to_idx   < 0 || ch->to_idx   >= f->cell_count) {
            fprintf(stderr, "[POST] FAIL: channel %d has invalid endpoint\n", i);
            ok = 0;
        }
    }

    /* POST-3: at least one output cell */
    int has_output = 0;
    for (int i = 0; i < f->cell_count; i++) {
        if (f->cells[i].is_output) { has_output = 1; break; }
    }
    if (!has_output) {
        fprintf(stderr, "[POST] WARN: no output cells defined — response will be empty\n");
    }

    /* POST-4: stable_core cells must have confidence >= 0.9 */
    for (int i = 0; i < f->cell_count; i++) {
        Cell *c = &f->cells[i];
        if (c->trust == TRUST_STABLE_CORE && c->confidence < 0.9f) {
            fprintf(stderr, "[POST] WARN: stable_core cell '%s' has low confidence %.2f\n",
                    c->label, c->confidence);
        }
    }

    if (ok) fprintf(stderr, "[BIOS] POST passed. %d cells, %d channels.\n",
                    f->cell_count, f->channel_count);
    return ok;
}

void bios_register_interrupts(Field *f) {
    for (int i = 0; i < INT_COUNT; i++) f->interrupt_cells[i] = -1;
    for (int i = 0; i < f->cell_count; i++) {
        int iid = f->cells[i].interrupt_id;
        if (iid >= 0 && iid < INT_COUNT) {
            f->interrupt_cells[iid] = i;
        }
    }
}

int bios_boot(Field *f) {
    /* Boot order: Ring 0 first (stable_core), then outward */
    Trust boot_order[TRUST_COUNT] = {
        TRUST_STABLE_CORE,
        TRUST_PROJECT_CONSTRAINT,
        TRUST_EPISODIC,
        TRUST_PROSE_VOICE,
        TRUST_INTERPRETIVE,
        TRUST_REVIEW_ONLY,
    };

    for (int r = 0; r < TRUST_COUNT; r++) {
        Trust ring = boot_order[r];
        for (int i = 0; i < f->cell_count; i++) {
            Cell *c = &f->cells[i];
            if (c->trust != ring) continue;
            c->state    = STATE_RESTING;
            c->potential = c->resting;
            c->refractory_ticks = 0;
        }
    }

    /* Collect output cells sorted by priority */
    f->output_count = 0;
    for (int i = 0; i < f->cell_count; i++) {
        if (f->cells[i].is_output) {
            if (f->output_count < MAX_OUTPUTS)
                f->output_cells[f->output_count++] = i;
        }
    }

    bios_register_interrupts(f);

    f->booted        = 1;
    f->tick          = 0;
    f->global_energy = 0.0f;
    f->energy_floor  = 0.05f;

    fprintf(stderr, "[BIOS] boot complete. %d output cells registered.\n",
            f->output_count);
    return 1;
}

/* ═══════════════════════════════════════════════════════════════════════════
 * INTERRUPT HANDLING
 * ═══════════════════════════════════════════════════════════════════════════ */

void interrupt_raise(Field *f, InterruptVector v, int source_cell) {
    int handler = f->interrupt_cells[(int)v];
    if (handler < 0) return;  /* no handler registered */

    const char *names[] = {
        "CONTRADICTS_FIRED", "REVIEW_ONLY_APPROACHED",
        "ENERGY_DEPLETED", "TRUST_FLOOR_VIOLATED", "CRYSTALLIZE_THRESHOLD"
    };
    fprintf(stderr, "[INT] %s raised from cell %d ('%s')\n",
            names[(int)v], source_cell,
            source_cell >= 0 ? f->cells[source_cell].label : "system");

    /* Inject a strong excitatory pulse into the handler cell */
    cell_integrate(f, handler, 2.0f);
}

/* ═══════════════════════════════════════════════════════════════════════════
 * CELL OPERATIONS
 * ═══════════════════════════════════════════════════════════════════════════ */

void cell_integrate(Field *f, int idx, float input) {
    Cell *c = &f->cells[idx];
    if (c->state == STATE_REFRACTORY) return;
    if (c->trust == TRUST_REVIEW_ONLY) {
        interrupt_raise(f, INT_REVIEW_ONLY_APPROACHED, idx);
        return;
    }
    c->potential += input;
    if (c->state == STATE_RESTING) c->state = STATE_INTEGRATING;
}

void cell_fire(Field *f, int idx) {
    Cell *c = &f->cells[idx];
    c->state = STATE_FIRING;
    c->activation_count++;

    float amplitude = c->potential * c->confidence;

    /* Log to trace */
    if (f->trace_count < MAX_TRACE) {
        TraceEntry *te = &f->trace[f->trace_count++];
        te->tick              = f->tick;
        te->cell_idx          = idx;
        te->potential_at_fire = c->potential;
        te->amplitude_out     = amplitude;
        te->trust             = c->trust;
        strncpy(te->label, c->label, MAX_LABEL - 1);
    }

    /* Propagate to all outgoing channels */
    for (int ci = 0; ci < f->channel_count; ci++) {
        Channel *ch = &f->channels[ci];
        if (!ch->active || ch->from_idx != idx) continue;

        float sig = ch->weight * amplitude;
        if (ch->polarity == CHAN_INHIBITORY) sig = -sig;

        /* Stochastic release: weight is release probability */
        if (ch->type == CHAN_STOCHASTIC) {
            float r = (float)rand() / (float)RAND_MAX;
            if (r > ch->weight) continue;
            sig = amplitude;
        }

        if (ch->type == CHAN_DELAYED && ch->delay > 0) {
            /* Queue as wave */
            if (f->wave_count < MAX_WAVES) {
                Wave *w = &f->waves[f->wave_count++];
                w->origin_idx   = idx;
                w->target_idx   = ch->to_idx;
                w->amplitude    = sig;
                w->arrival_tick = f->tick + ch->delay;
                w->consumed     = 0;
            }
        } else {
            /* Immediate — also log satellite co-activation */
            satellite_observe(f, idx, ch->to_idx, f->tick);
            cell_integrate(f, ch->to_idx, sig);
        }
    }

    /* Reset after firing */
    c->potential        = c->resting;
    c->refractory_ticks = c->refractory_period;
    c->state            = STATE_REFRACTORY;

    /* Check crystallize threshold — output cell fired with high confidence */
    if (c->is_output && c->confidence >= 0.95f) {
        c->state = STATE_CRYSTALLIZED;
        interrupt_raise(f, INT_CRYSTALLIZE_THRESHOLD, idx);
    }
}

/* ═══════════════════════════════════════════════════════════════════════════
 * FIELD SIMULATION
 * ═══════════════════════════════════════════════════════════════════════════ */

void field_inject(Field *f, const char *keyword, float amplitude) {
    /* Find cells whose label or tags contain the keyword */
    for (int i = 0; i < f->cell_count; i++) {
        Cell *c = &f->cells[i];
        if (c->trust == TRUST_REVIEW_ONLY) continue;

        int match = 0;
        if (strstr(c->label, keyword)) match = 1;
        for (int t = 0; t < c->tag_count && !match; t++) {
            if (strstr(c->tags[t], keyword)) match = 1;
        }
        if (strstr(c->summary, keyword)) match = 1;

        if (match) cell_integrate(f, i, amplitude);
    }
}

void field_tick(Field *f) {
    f->tick++;
    f->global_energy = 0.0f;

    /* Deliver waves that arrive this tick */
    for (int i = 0; i < f->wave_count; i++) {
        Wave *w = &f->waves[i];
        if (!w->consumed && w->arrival_tick <= f->tick) {
            satellite_observe(f, w->origin_idx, w->target_idx, f->tick);
            cell_integrate(f, w->target_idx, w->amplitude);
            w->consumed = 1;
        }
    }

    /* Process cells: fire if threshold crossed; decay if not */
    for (int i = 0; i < f->cell_count; i++) {
        Cell *c = &f->cells[i];

        if (c->state == STATE_REFRACTORY) {
            c->refractory_ticks--;
            if (c->refractory_ticks <= 0) {
                c->state = STATE_RESTING;
                c->potential = c->resting;
            }
            continue;
        }

        if (c->state == STATE_CRYSTALLIZED) {
            f->global_energy += c->potential;
            continue;
        }

        if (c->potential >= c->threshold) {
            cell_fire(f, i);
        } else if (c->state == STATE_INTEGRATING) {
            /* Decay toward resting */
            c->potential = c->resting + (c->potential - c->resting) * c->decay;
            if (fabsf(c->potential - c->resting) < 1e-4f) {
                c->potential = c->resting;
                c->state     = STATE_RESTING;
            }
        }

        f->global_energy += fabsf(c->potential);
    }

    /* Energy depletion interrupt */
    if (f->global_energy < f->energy_floor && f->tick > 1) {
        interrupt_raise(f, INT_ENERGY_DEPLETED, -1);
    }
}

int field_run(Field *f, int max_ticks, float convergence_threshold) {
    int crystallized_last = 0;
    for (int t = 0; t < max_ticks; t++) {
        field_tick(f);

        /* Count crystallized output cells */
        int cryst = 0;
        for (int i = 0; i < f->output_count; i++) {
            if (f->cells[f->output_cells[i]].state == STATE_CRYSTALLIZED) cryst++;
        }

        /* Convergence: output cells crystallized and energy is low */
        if (cryst > 0 && f->global_energy < convergence_threshold) {
            fprintf(stderr, "[field] converged at tick %d  energy=%.4f  crystallized=%d\n",
                    f->tick, f->global_energy, cryst);
            return t + 1;
        }

        crystallized_last = cryst;
    }
    fprintf(stderr, "[field] max_ticks reached  tick=%d  energy=%.4f  crystallized=%d\n",
            f->tick, f->global_energy, crystallized_last);
    return max_ticks;
}

/* ═══════════════════════════════════════════════════════════════════════════
 * SATELLITE — Hebbian observer
 * ═══════════════════════════════════════════════════════════════════════════ */

void satellite_observe(Field *f, int cell_a, int cell_b, int tick) {
    if (f->satellite_count >= MAX_TRACE * 4) return;
    SatelliteEntry *e = &f->satellite[f->satellite_count++];
    e->tick       = tick;
    e->cell_a     = cell_a;
    e->cell_b     = cell_b;
    e->delta_weight = 0.01f;  /* base Hebbian delta */
    if (cell_a >= 0) strncpy(e->label_a, f->cells[cell_a].label, MAX_LABEL - 1);
    if (cell_b >= 0) strncpy(e->label_b, f->cells[cell_b].label, MAX_LABEL - 1);
}

void satellite_apply_hebbian(Field *f) {
    /* For each co-activation, strengthen the channel between them */
    for (int i = 0; i < f->satellite_count; i++) {
        SatelliteEntry *e = &f->satellite[i];
        for (int ci = 0; ci < f->channel_count; ci++) {
            Channel *ch = &f->channels[ci];
            if (ch->from_idx == e->cell_a && ch->to_idx == e->cell_b) {
                ch->weight += e->delta_weight;
                if (ch->weight > 1.0f) ch->weight = 1.0f;
            }
        }
        /* Track on the cell itself */
        if (e->cell_a >= 0) f->cells[e->cell_a].co_activation_weight += e->delta_weight;
        if (e->cell_b >= 0) f->cells[e->cell_b].co_activation_weight += e->delta_weight;
    }
}

void satellite_debrief(Field *f) {
    fprintf(stdout, "\n[SATELLITE DEBRIEF]\n");
    fprintf(stdout, "Ticks: %d   Co-activations: %d\n", f->tick, f->satellite_count);
    fprintf(stdout, "Top activated cells:\n");

    /* Find top 5 by activation count */
    int order[MAX_CELLS];
    for (int i = 0; i < f->cell_count; i++) order[i] = i;
    for (int i = 0; i < f->cell_count - 1; i++) {
        for (int j = i + 1; j < f->cell_count; j++) {
            if (f->cells[order[j]].activation_count > f->cells[order[i]].activation_count) {
                int tmp = order[i]; order[i] = order[j]; order[j] = tmp;
            }
        }
    }
    for (int i = 0; i < 5 && i < f->cell_count; i++) {
        Cell *c = &f->cells[order[i]];
        if (c->activation_count == 0) break;
        fprintf(stdout, "  %3dx  %-30s  trust=%-20s  confidence=%.2f\n",
                c->activation_count, c->label,
                trust_to_string(c->trust), c->confidence);
    }

    if (f->satellite_count > 0) {
        fprintf(stdout, "Most recent co-activations:\n");
        int start = f->satellite_count > 5 ? f->satellite_count - 5 : 0;
        for (int i = start; i < f->satellite_count; i++) {
            SatelliteEntry *e = &f->satellite[i];
            fprintf(stdout, "  t=%3d  %-25s <-> %-25s  Δ=%.3f\n",
                    e->tick, e->label_a, e->label_b, e->delta_weight);
        }
    }
    fprintf(stdout, "[/SATELLITE DEBRIEF]\n\n");
}

/* ═══════════════════════════════════════════════════════════════════════════
 * RESPONSE RENDERING
 * ═══════════════════════════════════════════════════════════════════════════ */

/* Compare output cells by priority then activation */
static int cmp_output(const void *a, const void *b, void *ctx) {
    Field *f = (Field *)ctx;
    int ia = *(const int *)a;
    int ib = *(const int *)b;
    Cell *ca = &f->cells[ia];
    Cell *cb = &f->cells[ib];
    if (ca->output_priority != cb->output_priority)
        return ca->output_priority - cb->output_priority;
    return cb->activation_count - ca->activation_count;
}

void render_response(Field *f) {
    /* Sort output cells */
    /* Simple insertion sort (no qsort_r on Windows MSVC, but gcc has it) */
    for (int i = 1; i < f->output_count; i++) {
        int key = f->output_cells[i];
        int j = i - 1;
        while (j >= 0 && cmp_output(&f->output_cells[j], &key, f) > 0) {
            f->output_cells[j + 1] = f->output_cells[j];
            j--;
        }
        f->output_cells[j + 1] = key;
    }

    fprintf(stdout, "\n[RESPONSE]\n");
    int printed = 0;
    for (int i = 0; i < f->output_count; i++) {
        Cell *c = &f->cells[f->output_cells[i]];
        if (c->activation_count == 0 && c->state != STATE_CRYSTALLIZED) continue;
        if (c->trust == TRUST_REVIEW_ONLY) continue;
        if (c->summary[0]) {
            fprintf(stdout, "%s\n", c->summary);
            printed++;
        }
    }
    if (!printed) {
        fprintf(stdout, "(no output cells activated — field did not converge on a response)\n");
    }
    fprintf(stdout, "[/RESPONSE]\n");
}

/* ═══════════════════════════════════════════════════════════════════════════
 * FIELD STATE DUMP (debug)
 * ═══════════════════════════════════════════════════════════════════════════ */

void field_dump_state(Field *f) {
    fprintf(stderr, "\n[FIELD STATE] tick=%d  energy=%.4f\n", f->tick, f->global_energy);
    for (int i = 0; i < f->cell_count; i++) {
        Cell *c = &f->cells[i];
        if (c->potential == c->resting && c->activation_count == 0) continue;
        const char *state_names[] = {"REST","INTEG","FIRE","REFRAC","CRYST"};
        fprintf(stderr, "  %-30s  V=%.3f  state=%-6s  fired=%dx  trust=%s\n",
                c->label, c->potential,
                state_names[(int)c->state], c->activation_count,
                trust_to_string(c->trust));
    }
    fprintf(stderr, "\n");
}

/* ═══════════════════════════════════════════════════════════════════════════
 * MAIN
 * ═══════════════════════════════════════════════════════════════════════════ */

static void usage(const char *prog) {
    fprintf(stderr,
        "Usage: %s <model_dir> [query words...]\n"
        "       %s <model_dir> --file <query_file>\n"
        "\n"
        "There are no instructions. There are only responses.\n"
        "\n"
        "  model_dir   directory containing .cog files\n"
        "  query       words to inject as field pulses\n"
        "\n"
        "Options:\n"
        "  --ticks N       max simulation ticks (default 32)\n"
        "  --amplitude F   injection amplitude (default 1.5)\n"
        "  --dump          dump field state after simulation\n"
        "  --debrief       print satellite debrief\n"
        "  --hebbian       apply Hebbian updates after run\n"
        "\n",
        prog, prog);
}

int main(int argc, char *argv[]) {
    srand((unsigned)time(NULL));

    if (argc < 2) { usage(argv[0]); return 1; }

    const char *model_dir = argv[1];
    int max_ticks = 32;
    float amplitude = 1.5f;
    int do_dump    = 0;
    int do_debrief = 1;
    int do_hebbian = 0;
    const char *query_file = NULL;

    /* Query words collected here */
    char query_words[64][256];
    int  query_count = 0;

    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "--ticks") == 0 && i+1 < argc) {
            max_ticks = atoi(argv[++i]);
        } else if (strcmp(argv[i], "--amplitude") == 0 && i+1 < argc) {
            amplitude = (float)atof(argv[++i]);
        } else if (strcmp(argv[i], "--dump") == 0) {
            do_dump = 1;
        } else if (strcmp(argv[i], "--no-debrief") == 0) {
            do_debrief = 0;
        } else if (strcmp(argv[i], "--hebbian") == 0) {
            do_hebbian = 1;
        } else if (strcmp(argv[i], "--file") == 0 && i+1 < argc) {
            query_file = argv[++i];
        } else if (argv[i][0] != '-') {
            if (query_count < 64) strncpy(query_words[query_count++], argv[i], 255);
        }
    }

    /* Load query from file if specified */
    char file_query[4096] = {0};
    if (query_file) {
        char *content = read_file(query_file);
        if (content) {
            strncpy(file_query, content, 4095);
            free(content);
            /* Tokenize on whitespace */
            char *tok = strtok(file_query, " \t\n\r");
            while (tok && query_count < 64) {
                strncpy(query_words[query_count++], tok, 255);
                tok = strtok(NULL, " \t\n\r");
            }
        }
    }

    if (query_count == 0) {
        fprintf(stderr, "[cog] no query provided\n");
        usage(argv[0]);
        return 1;
    }

    /* Initialize field */
    Field *f = calloc(1, sizeof(Field));
    if (!f) { fprintf(stderr, "[cog] out of memory\n"); return 1; }
    for (int i = 0; i < INT_COUNT; i++) f->interrupt_cells[i] = -1;

    /* Load model */
    fprintf(stderr, "[BIOS] loading model from: %s\n", model_dir);
    int loaded = cog_load_dir(f, model_dir);

    /* Also try model/cells/ subdirectory */
    char cells_dir[512];
    snprintf(cells_dir, sizeof(cells_dir), "%s/cells", model_dir);
    loaded += cog_load_dir(f, cells_dir);

    if (loaded == 0) {
        fprintf(stderr, "[cog] no .cog files found in: %s\n", model_dir);
        free(f);
        return 1;
    }

    /* POST */
    if (!bios_post(f)) {
        fprintf(stderr, "[BIOS] POST failed — field may be inconsistent\n");
    }

    /* Boot */
    bios_boot(f);

    /* Inject query as field pulses */
    fprintf(stderr, "[field] injecting %d query words at amplitude %.2f\n",
            query_count, amplitude);
    for (int i = 0; i < query_count; i++) {
        field_inject(f, query_words[i], amplitude);
    }

    /* Run simulation */
    field_run(f, max_ticks, 0.01f);

    if (do_dump) field_dump_state(f);

    /* Render response */
    render_response(f);

    /* Satellite */
    if (do_debrief) satellite_debrief(f);
    if (do_hebbian) satellite_apply_hebbian(f);

    free(f);
    return 0;
}
