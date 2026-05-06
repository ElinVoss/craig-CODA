/*
 * cog.h — Field Computation Substrate
 *
 * There are no instructions. There are only responses.
 *
 * The cell network IS the model.
 * Field simulation IS inference.
 * The satellite Hebbian loop IS training.
 */

#ifndef COG_H
#define COG_H

#include <stdint.h>
#include <stddef.h>

/* ── Limits ─────────────────────────────────────────────────────────────── */
#define MAX_CELLS       2048
#define MAX_CHANNELS    8192
#define MAX_WAVES        512
#define MAX_TRACE        256
#define MAX_LABEL         64
#define MAX_TAG_LEN       32
#define MAX_TAGS          16
#define MAX_TRIGGERS      16
#define MAX_OUTPUTS       32
#define MAX_FILES         64
#define MAX_INTERRUPTS    16

/* ── Enumerations ───────────────────────────────────────────────────────── */

/* Trust layer — maps to privilege ring (Ring 0 = stable_core) */
typedef enum {
    TRUST_STABLE_CORE        = 0,   /* Ring 0 — identity, never overwritten */
    TRUST_PROJECT_CONSTRAINT = 1,   /* Ring 1 — hard constraints            */
    TRUST_EPISODIC           = 2,   /* Ring 2 — events, temporal facts      */
    TRUST_PROSE_VOICE        = 3,   /* Ring 3 — style, register             */
    TRUST_INTERPRETIVE       = 4,   /* Ring 4 — hypotheses, soft frames     */
    TRUST_REVIEW_ONLY        = 5,   /* Ring 5 — protected, never surface    */
    TRUST_COUNT              = 6
} Trust;

/* Cell state in the activation cycle */
typedef enum {
    STATE_RESTING      = 0,
    STATE_INTEGRATING  = 1,
    STATE_FIRING       = 2,
    STATE_REFRACTORY   = 3,
    STATE_CRYSTALLIZED = 4   /* stable response — output eligible */
} CellState;

/* Channel polarity */
typedef enum {
    CHAN_EXCITATORY = 0,
    CHAN_INHIBITORY = 1
} Polarity;

/* Channel type */
typedef enum {
    CHAN_DIRECT   = 0,   /* fixed weight, immediate */
    CHAN_DELAYED  = 1,   /* fixed delay in ticks    */
    CHAN_STOCHASTIC = 2  /* weight is release probability */
} ChanType;

/* Interrupt vector indices */
typedef enum {
    INT_CONTRADICTS_FIRED      = 0,
    INT_REVIEW_ONLY_APPROACHED = 1,
    INT_ENERGY_DEPLETED        = 2,
    INT_TRUST_FLOOR_VIOLATED   = 3,
    INT_CRYSTALLIZE_THRESHOLD  = 4,
    INT_COUNT                  = 5
} InterruptVector;

/* ── Core data structures ───────────────────────────────────────────────── */

typedef struct Cell {
    char     label[MAX_LABEL];
    Trust    trust;
    CellState state;

    float    threshold;       /* fire when potential >= threshold     */
    float    potential;       /* current membrane potential           */
    float    resting;         /* potential decays toward this         */
    float    decay;           /* potential decay per tick (0..1)      */
    float    confidence;      /* node confidence (affects output weight) */

    int      refractory_ticks;  /* ticks remaining in refractory period */
    int      refractory_period; /* how long refractory lasts            */

    char     tags[MAX_TAGS][MAX_TAG_LEN];
    int      tag_count;

    char     summary[256];    /* human-readable summary (for satellite log) */
    float    voice_score;     /* prose register score                       */

    /* Output cell fields */
    int      is_output;       /* 1 if this cell contributes to response      */
    int      output_priority; /* lower = higher priority in response         */

    /* Interrupt cell fields */
    int      interrupt_id;    /* -1 if not an interrupt cell                 */

    /* Reinforcement */
    int      activation_count;
    float    co_activation_weight;  /* Hebbian accumulated weight            */
} Cell;


typedef struct Channel {
    int      from_idx;   /* index into field->cells */
    int      to_idx;
    Polarity polarity;
    ChanType type;
    float    weight;
    int      delay;      /* ticks, for CHAN_DELAYED */
    int      active;     /* 1 = enabled            */
} Channel;


typedef struct Wave {
    int      origin_idx;   /* cell that fired         */
    int      target_idx;   /* cell receiving the wave */
    float    amplitude;
    int      arrival_tick; /* when it lands           */
    int      consumed;
} Wave;


typedef struct TraceEntry {
    int   tick;
    int   cell_idx;
    float potential_at_fire;
    float amplitude_out;
    char  label[MAX_LABEL];
    Trust trust;
} TraceEntry;


typedef struct SatelliteEntry {
    int   tick;
    int   cell_a;
    int   cell_b;
    float delta_weight;   /* Hebbian update */
    char  label_a[MAX_LABEL];
    char  label_b[MAX_LABEL];
} SatelliteEntry;


typedef struct {
    Cell         cells[MAX_CELLS];
    int          cell_count;

    Channel      channels[MAX_CHANNELS];
    int          channel_count;

    Wave         waves[MAX_WAVES];
    int          wave_count;

    TraceEntry   trace[MAX_TRACE];
    int          trace_count;

    SatelliteEntry satellite[MAX_TRACE * 4];
    int          satellite_count;

    /* Output rendering */
    int          output_cells[MAX_OUTPUTS];
    int          output_count;

    /* Interrupt vector — cell indices, -1 if unregistered */
    int          interrupt_cells[INT_COUNT];

    /* Boot state */
    int          booted;
    int          tick;
    float        global_energy;   /* total potential across all cells      */
    float        energy_floor;    /* interrupt fires if below this          */
} Field;


/* ── Function declarations ──────────────────────────────────────────────── */

/* Lexer / Parser */
int  cog_load_file(Field *f, const char *path);
int  cog_load_dir(Field *f, const char *dir_path);

/* BIOS */
int  bios_post(Field *f);
int  bios_boot(Field *f);
void bios_register_interrupts(Field *f);

/* Field simulation */
void field_inject(Field *f, const char *keyword, float amplitude);
void field_tick(Field *f);
int  field_run(Field *f, int max_ticks, float convergence_threshold);

/* Cell operations */
int  cell_find(Field *f, const char *label);
void cell_fire(Field *f, int idx);
void cell_integrate(Field *f, int idx, float input);

/* Interrupt handling */
void interrupt_raise(Field *f, InterruptVector v, int source_cell);

/* Satellite */
void satellite_observe(Field *f, int cell_a, int cell_b, int tick);
void satellite_apply_hebbian(Field *f);
void satellite_debrief(Field *f);

/* Response rendering */
void render_response(Field *f);

/* Utilities */
Trust trust_from_string(const char *s);
const char *trust_to_string(Trust t);
CellState state_from_string(const char *s);
void field_dump_state(Field *f);

#endif /* COG_H */
