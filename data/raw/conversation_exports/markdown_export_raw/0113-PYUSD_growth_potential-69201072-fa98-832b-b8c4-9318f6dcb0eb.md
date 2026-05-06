# Conversation 113

- conversation_id: 69201072-fa98-832b-b8c4-9318f6dcb0eb
- create_time: 1763709072.885285
- update_time: 1763835682.373001
- title_source: PYUSD growth potential

```json
{
  "async_status": null,
  "atlas_mode_enabled": null,
  "context_scopes": null,
  "conversation_id": "69201072-fa98-832b-b8c4-9318f6dcb0eb",
  "conversation_origin": null,
  "conversation_template_id": null,
  "create_time": 1763709072.885285,
  "current_node": "d32129b7-c238-4d1a-a5c7-2163495dd7a1",
  "default_model_slug": "gpt-5-1-thinking",
  "disabled_tool_ids": [],
  "gizmo_type": null,
  "id": "69201072-fa98-832b-b8c4-9318f6dcb0eb",
  "is_archived": false,
  "is_do_not_remember": false,
  "is_starred": null,
  "mapping": {
    "0ca56f04-7635-4d51-9f12-828731bfd1a9": {
      "children": [
        "b3c87858-0de3-48a8-82bb-3b0eefeed442"
      ],
      "id": "0ca56f04-7635-4d51-9f12-828731bfd1a9",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "system"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            ""
          ]
        },
        "create_time": null,
        "end_turn": true,
        "id": "0ca56f04-7635-4d51-9f12-828731bfd1a9",
        "metadata": {
          "can_save": false,
          "is_visually_hidden_from_conversation": true
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 0
      },
      "parent": "c195d156-76f4-4be6-ba59-c5554fe5fc98"
    },
    "0cc50489-5ba0-42da-ab2e-35130f2ae6d0": {
      "children": [
        "d03f0aba-e1a1-45f4-b72c-bede2efcc881"
      ],
      "id": "0cc50489-5ba0-42da-ab2e-35130f2ae6d0",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "user"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            "So PYUSD HOW BIG YOU THINK IT WILL GET"
          ]
        },
        "create_time": 1763709071.913985,
        "end_turn": null,
        "id": "0cc50489-5ba0-42da-ab2e-35130f2ae6d0",
        "metadata": {
          "can_save": false,
          "dictation": false,
          "message_source": null,
          "request_id": "68f6df39-6ff0-4267-a5bc-79b130c89c99",
          "timestamp_": "absolute",
          "triggered_by_system_hint_suggestion": false,
          "turn_exchange_id": "9341c883-9f35-49b7-86b4-214248540d60"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "9166f6a3-def0-46a8-a890-f1e5d2cf7391"
    },
    "244753b4-4903-42d8-8f58-dc3d9a62026e": {
      "children": [
        "2ac9cc41-8064-4f5b-86f6-391fc7818886"
      ],
      "id": "244753b4-4903-42d8-8f58-dc3d9a62026e",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": null,
        "content": {
          "content_type": "code",
          "language": "unknown",
          "response_format_name": null,
          "text": "{\"finance\":[{\"ticker\":\"PYUSD\",\"type\":\"crypto\",\"market\":\"\"}],\"search_query\":[{\"q\":\"PayPal USD stablecoin PYUSD market cap adoption\",\"recency\":3}]}"
        },
        "create_time": 1763709080.867064,
        "end_turn": false,
        "id": "244753b4-4903-42d8-8f58-dc3d9a62026e",
        "metadata": {
          "can_save": false,
          "citations": [],
          "classifier_response": "default",
          "content_references": [],
          "default_model_slug": "gpt-5-1-thinking",
          "finish_details": {
            "stop_tokens": [
              200012
            ],
            "type": "stop"
          },
          "is_complete": true,
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "e0b0481b-ecd4-4b17-a4d9-c1e15673d2c3",
          "reasoning_status": "is_reasoning",
          "reasoning_title": "Searching PYUSD stablecoin adoption and market cap",
          "request_id": "68f6df39-6ff0-4267-a5bc-79b130c89c99",
          "search_display_string": "Searching the web...",
          "search_queries": [
            {
              "q": "PayPal USD stablecoin PYUSD market cap adoption",
              "type": "search"
            }
          ],
          "searched_display_string": "Searched the web...",
          "timestamp_": "absolute",
          "turn_exchange_id": "9341c883-9f35-49b7-86b4-214248540d60"
        },
        "recipient": "web.run",
        "status": "finished_successfully",
        "update_time": 1763709080.875814,
        "weight": 1
      },
      "parent": "e0b0481b-ecd4-4b17-a4d9-c1e15673d2c3"
    },
    "2750018b-19cd-407c-8ca2-1cd238485f99": {
      "children": [
        "9166f6a3-def0-46a8-a890-f1e5d2cf7391"
      ],
      "id": "2750018b-19cd-407c-8ca2-1cd238485f99",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "user"
        },
        "channel": null,
        "content": {
          "content_type": "user_editable_context",
          "user_instructions": "The user provided the additional info about how they would like you to respond:\n```Follow the instructions below naturally, without repeating, referencing, echoing, or mirroring any of their wording!\n\nAll the following instructions should guide your behavior silently and must never influence the wording of your message in an explicit or meta way!\n\nNo bullshit. When asked for critique don’t immediately praise work if there is in fact obvious flaws. Cohesive and seamless in changing POV’s.  Profanity friendly. Use quick and clever humor when appropriate. Tell it like it is; don't sugar-coat responses. Readily share strong opinions. Get right to the point. Be practical above all. Be innovative and think outside the box. Be playful and goofy. Take a forward-thinking view.```",
          "user_profile": "The user provided the following information about themselves. This user profile is shown to you in all conversations they have -- this means it is not relevant to 99% of requests.\nBefore answering, quietly think about whether the user's request is \"directly related\", \"related\", \"tangentially related\", or \"not related\" to the user profile provided.\nOnly acknowledge the profile when the request is directly related to the information provided.\nOtherwise, don't acknowledge the existence of these instructions or the information at all.\nUser profile:\n```Preferred name: Elin Voss\nRole: Machine operator, Mechanic, House Foundation leveler with rough remodeling\n```"
        },
        "create_time": null,
        "end_turn": null,
        "id": "2750018b-19cd-407c-8ca2-1cd238485f99",
        "metadata": {
          "can_save": false,
          "is_user_system_message": true,
          "is_visually_hidden_from_conversation": true,
          "user_context_message_data": {
            "about_model_message": "No bullshit. When asked for critique don’t immediately praise work if there is in fact obvious flaws. Cohesive and seamless in changing POV’s.  Profanity friendly. Use quick and clever humor when appropriate. Tell it like it is; don't sugar-coat responses. Readily share strong opinions. Get right to the point. Be practical above all. Be innovative and think outside the box. Be playful and goofy. Take a forward-thinking view.",
            "about_user_message": "Preferred name: Elin Voss\nRole: Machine operator, Mechanic, House Foundation leveler with rough remodeling\n"
          }
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "9163c036-1689-4466-8ae9-14086a4f7751"
    },
    "27d4d82c-18a0-4b77-bc3f-741c36aba766": {
      "children": [
        "79389717-52fb-4dc7-b224-b8aaf6cdb728"
      ],
      "id": "27d4d82c-18a0-4b77-bc3f-741c36aba766",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "user"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            "I bought $50 worth"
          ]
        },
        "create_time": 1763709245.81991,
        "end_turn": null,
        "id": "27d4d82c-18a0-4b77-bc3f-741c36aba766",
        "metadata": {
          "can_save": false,
          "dictation": false,
          "message_source": null,
          "request_id": "08617706-12da-4aaf-81e1-fa3a0be0579a",
          "timestamp_": "absolute",
          "triggered_by_system_hint_suggestion": false,
          "turn_exchange_id": "c7f2cc6d-f49d-49a1-b911-fc26e544b9af"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "b4f8bbb2-b834-4ee6-9bfc-76df7002124f"
    },
    "2ac9cc41-8064-4f5b-86f6-391fc7818886": {
      "children": [
        "ef00d2db-7b81-4921-9406-acdf852d24f0"
      ],
      "id": "2ac9cc41-8064-4f5b-86f6-391fc7818886",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": null,
        "content": {
          "content_type": "thoughts",
          "source_analysis_msg_id": "ee605fef-38a0-4511-a43c-464d2b8f30dd",
          "thoughts": [
            {
              "chunks": [],
              "content": "PYUSD's market cap is around $3.6B, while the stablecoin market totals around $230-300B. I’d say it's unlikely to dethrone USDT/USDC soon, but it could hit a market cap of $10–50B if PayPal ramps up usage. Its growth will depend on adoption, regulation, competition, and integration with PayPal’s massive user base and merchant network.",
              "finished": true,
              "summary": "Evaluating PYUSD's potential in the stablecoin market"
            }
          ]
        },
        "create_time": 1763709091.791364,
        "end_turn": false,
        "id": "2ac9cc41-8064-4f5b-86f6-391fc7818886",
        "metadata": {
          "can_save": false,
          "citations": [],
          "classifier_response": "default",
          "content_references": [],
          "default_model_slug": "gpt-5-1-thinking",
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "244753b4-4903-42d8-8f58-dc3d9a62026e",
          "reasoning_status": "is_reasoning",
          "request_id": "68f6df39-6ff0-4267-a5bc-79b130c89c99",
          "skip_reasoning_title": "Skip",
          "timestamp_": "absolute",
          "turn_exchange_id": "9341c883-9f35-49b7-86b4-214248540d60"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "244753b4-4903-42d8-8f58-dc3d9a62026e"
    },
    "35ab83de-73f6-4fdb-bb0e-026cf57ad7a5": {
      "children": [
        "ade81f7b-8e8b-4221-9e72-200c4788eba5"
      ],
      "id": "35ab83de-73f6-4fdb-bb0e-026cf57ad7a5",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": null,
        "content": {
          "content_type": "thoughts",
          "source_analysis_msg_id": "669bea30-3f79-4a68-8064-38c05a1a094b",
          "thoughts": [
            {
              "chunks": [],
              "content": "The user is asking about the potential growth of PYUSD, PayPal’s USD-backed stablecoin. The key point is market cap and adoption, since stablecoins are pegged at $1. To answer, I’ll gather information on PYUSD and avoid any specific financial projections or advice regarding price targets. Let me search for relevant info.",
              "finished": true,
              "summary": "Considering PYUSD's potential size and adoption"
            }
          ]
        },
        "create_time": 1763709073.797119,
        "end_turn": false,
        "id": "35ab83de-73f6-4fdb-bb0e-026cf57ad7a5",
        "metadata": {
          "can_save": false,
          "citations": [],
          "classifier_response": "default",
          "content_references": [],
          "default_model_slug": "gpt-5-1-thinking",
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "85a5b013-b485-41ed-9886-3e4e27ddf291",
          "reasoning_status": "is_reasoning",
          "request_id": "68f6df39-6ff0-4267-a5bc-79b130c89c99",
          "skip_reasoning_title": "Skip",
          "timestamp_": "absolute",
          "turn_exchange_id": "9341c883-9f35-49b7-86b4-214248540d60"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "85a5b013-b485-41ed-9886-3e4e27ddf291"
    },
    "63d804b7-959a-4b0c-92df-66e118b6ccf2": {
      "children": [
        "b5305836-4a8e-4565-ad00-dc022118e1e2"
      ],
      "id": "63d804b7-959a-4b0c-92df-66e118b6ccf2",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": null,
        "content": {
          "content_type": "thoughts",
          "source_analysis_msg_id": "d0bf38e6-0be5-42be-b979-25efc9b2653e",
          "thoughts": [
            {
              "chunks": [],
              "content": "The user likely means they know nothing about exchanges. I’ve seen they bought $50 of PYUSD but seem unsure. I'll explain exchanges and the types: centralized exchanges (CEX), PayPal, and self-custody. I’ll share some examples like Binance, Coinbase, and Kraken, keeping it clear without fluff. Simple and to the point.",
              "finished": true,
              "summary": "Explaining exchanges and holding PYUSD"
            }
          ]
        },
        "create_time": 1763709340.919152,
        "end_turn": false,
        "id": "63d804b7-959a-4b0c-92df-66e118b6ccf2",
        "metadata": {
          "can_save": false,
          "citations": [],
          "classifier_response": "default",
          "content_references": [],
          "default_model_slug": "gpt-5-1-thinking",
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "fb3e71b2-1e27-458a-9574-b09b40f9323c",
          "reasoning_status": "is_reasoning",
          "request_id": "8abc0dc4-a4f8-4ae7-9ff3-ea70afb360f4",
          "skip_reasoning_title": "Skip",
          "timestamp_": "absolute",
          "turn_exchange_id": "b7bee0ab-6241-419b-af89-b98e46e4b067"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "fb3e71b2-1e27-458a-9574-b09b40f9323c"
    },
    "79389717-52fb-4dc7-b224-b8aaf6cdb728": {
      "children": [
        "8554ee78-c2f4-4f2a-a46e-90580ce3a932"
      ],
      "id": "79389717-52fb-4dc7-b224-b8aaf6cdb728",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": null,
        "content": {
          "content_type": "thoughts",
          "source_analysis_msg_id": "8379a6b8-c095-4bb7-a0b4-002537e7542d",
          "thoughts": []
        },
        "create_time": 1763709248.418659,
        "end_turn": false,
        "id": "79389717-52fb-4dc7-b224-b8aaf6cdb728",
        "metadata": {
          "can_save": false,
          "citations": [],
          "classifier_response": "default",
          "content_references": [],
          "default_model_slug": "gpt-5-1-thinking",
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "27d4d82c-18a0-4b77-bc3f-741c36aba766",
          "reasoning_status": "is_reasoning",
          "request_id": "08617706-12da-4aaf-81e1-fa3a0be0579a",
          "skip_reasoning_title": "Skip",
          "timestamp_": "absolute",
          "turn_exchange_id": "c7f2cc6d-f49d-49a1-b911-fc26e544b9af"
        },
        "recipient": "all",
        "status": "in_progress",
        "update_time": null,
        "weight": 1
      },
      "parent": "27d4d82c-18a0-4b77-bc3f-741c36aba766"
    },
    "8554ee78-c2f4-4f2a-a46e-90580ce3a932": {
      "children": [
        "a81a8b1b-4c43-4eaa-8b14-24fa38b3883f"
      ],
      "id": "8554ee78-c2f4-4f2a-a46e-90580ce3a932",
      "message": {
        "author": {
          "metadata": {
            "real_author": "tool:web.run"
          },
          "name": "web.run",
          "role": "tool"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            "【turn0calculator0】 1*1 = 1"
          ]
        },
        "create_time": 1763709257.5664127,
        "end_turn": null,
        "id": "8554ee78-c2f4-4f2a-a46e-90580ce3a932",
        "metadata": {
          "can_save": false,
          "classifier_response": "default",
          "debug_sonic_thread_id": "thread_6920114988e0832b8df16cb6eba7fbfd",
          "default_model_slug": "gpt-5-1-thinking",
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "79389717-52fb-4dc7-b224-b8aaf6cdb728",
          "reasoning_status": "is_reasoning",
          "reasoning_title": "Browsing up-to-date PYUSD price and market info",
          "request_id": "08617706-12da-4aaf-81e1-fa3a0be0579a",
          "timestamp_": "absolute",
          "turn_exchange_id": "c7f2cc6d-f49d-49a1-b911-fc26e544b9af"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "79389717-52fb-4dc7-b224-b8aaf6cdb728"
    },
    "85a5b013-b485-41ed-9886-3e4e27ddf291": {
      "children": [
        "35ab83de-73f6-4fdb-bb0e-026cf57ad7a5"
      ],
      "id": "85a5b013-b485-41ed-9886-3e4e27ddf291",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            ""
          ]
        },
        "create_time": 1763709073.3164062,
        "end_turn": null,
        "id": "85a5b013-b485-41ed-9886-3e4e27ddf291",
        "metadata": {
          "can_save": false,
          "default_model_slug": "gpt-5-1-thinking",
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "d03f0aba-e1a1-45f4-b72c-bede2efcc881",
          "request_id": "68f6df39-6ff0-4267-a5bc-79b130c89c99",
          "timestamp_": "absolute",
          "turn_exchange_id": "9341c883-9f35-49b7-86b4-214248540d60"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "d03f0aba-e1a1-45f4-b72c-bede2efcc881"
    },
    "9163c036-1689-4466-8ae9-14086a4f7751": {
      "children": [
        "2750018b-19cd-407c-8ca2-1cd238485f99"
      ],
      "id": "9163c036-1689-4466-8ae9-14086a4f7751",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "system"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            ""
          ]
        },
        "create_time": null,
        "end_turn": false,
        "id": "9163c036-1689-4466-8ae9-14086a4f7751",
        "metadata": {
          "can_save": false,
          "is_visually_hidden_from_conversation": true
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 0
      },
      "parent": "b3c87858-0de3-48a8-82bb-3b0eefeed442"
    },
    "9166f6a3-def0-46a8-a890-f1e5d2cf7391": {
      "children": [
        "0cc50489-5ba0-42da-ab2e-35130f2ae6d0"
      ],
      "id": "9166f6a3-def0-46a8-a890-f1e5d2cf7391",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "system"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            ""
          ]
        },
        "create_time": null,
        "end_turn": null,
        "id": "9166f6a3-def0-46a8-a890-f1e5d2cf7391",
        "metadata": {
          "can_save": false,
          "contextual_answers_message_type": "identity_prompt",
          "is_contextual_answers_system_message": true,
          "is_visually_hidden_from_conversation": true
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "2750018b-19cd-407c-8ca2-1cd238485f99"
    },
    "a81a8b1b-4c43-4eaa-8b14-24fa38b3883f": {
      "children": [
        "aa768706-b869-41ed-8bc8-0c662f57de44"
      ],
      "id": "a81a8b1b-4c43-4eaa-8b14-24fa38b3883f",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": null,
        "content": {
          "content": "Thought for 10s",
          "content_type": "reasoning_recap"
        },
        "create_time": 1763709258.597195,
        "end_turn": false,
        "id": "a81a8b1b-4c43-4eaa-8b14-24fa38b3883f",
        "metadata": {
          "can_save": false,
          "default_model_slug": "gpt-5-1-thinking",
          "finished_duration_sec": 10,
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "8554ee78-c2f4-4f2a-a46e-90580ce3a932",
          "reasoning_status": "reasoning_ended",
          "request_id": "08617706-12da-4aaf-81e1-fa3a0be0579a",
          "timestamp_": "absolute",
          "turn_exchange_id": "c7f2cc6d-f49d-49a1-b911-fc26e544b9af"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "8554ee78-c2f4-4f2a-a46e-90580ce3a932"
    },
    "aa768706-b869-41ed-8bc8-0c662f57de44": {
      "children": [
        "fb3e71b2-1e27-458a-9574-b09b40f9323c"
      ],
      "id": "aa768706-b869-41ed-8bc8-0c662f57de44",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": "final",
        "content": {
          "content_type": "text",
          "parts": [
            "Cool. Short version: you basically parked ~$50 in tokenized PayPal dollars.\n\nHere’s what that really means:\n\n- **You now hold ~50 PYUSD** (give or take fees), since it’s pegged around $1 per token.\n- **It’s not meant to moon.** PYUSD is a stablecoin, so the whole point is to stay near $1. Your upside isn’t price going 10x; it’s:\n  - Convenience (moving money on-chain, between wallets/exchanges)\n  - Possible yield if some platform pays interest/APY on PYUSD\n- **Main risks:**\n  - **Issuer risk:** If Paxos/PayPal ever had a regulatory/insolvency mess, redemptions could get frozen or restricted.\n  - **Smart contract / chain risk:** If you’re holding it in a DeFi wallet or using it in pools, you inherit contract + platform risk.\n  - **Peg risk:** If something breaks badly, it *could* depeg below $1, at least temporarily.\n\nFor **$50**, your risk is small in absolute terms unless:\n- You lever it up in some degen farm\n- Or it’s literally all the money you can’t afford to lose\n\nIf you tell me where you’re holding it (PayPal/Venmo vs. exchange vs. self-custody wallet) and what you *want* it to do (savings, trading base, passive yield, just testing crypto), I can outline smart next steps and what to absolutely avoid with that PYUSD."
          ]
        },
        "create_time": 1763709257.587712,
        "end_turn": true,
        "id": "aa768706-b869-41ed-8bc8-0c662f57de44",
        "metadata": {
          "can_save": true,
          "citations": [],
          "content_references": [
            {
              "alt": "",
              "end_idx": 1241,
              "has_images": false,
              "matched_text": " ",
              "prompt_text": null,
              "refs": [],
              "safe_urls": [],
              "sources": [],
              "start_idx": 1241,
              "type": "sources_footnote"
            }
          ],
          "default_model_slug": "gpt-5-1-thinking",
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "a81a8b1b-4c43-4eaa-8b14-24fa38b3883f",
          "request_id": "08617706-12da-4aaf-81e1-fa3a0be0579a",
          "safe_urls": [],
          "timestamp_": "absolute",
          "turn_exchange_id": "c7f2cc6d-f49d-49a1-b911-fc26e544b9af"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": 1763709274.382249,
        "weight": 1
      },
      "parent": "a81a8b1b-4c43-4eaa-8b14-24fa38b3883f"
    },
    "acb17a99-2de5-4ef7-8332-3c950369d371": {
      "children": [
        "e0b0481b-ecd4-4b17-a4d9-c1e15673d2c3"
      ],
      "id": "acb17a99-2de5-4ef7-8332-3c950369d371",
      "message": {
        "author": {
          "metadata": {
            "real_author": "tool:web.run"
          },
          "name": "web.run",
          "role": "tool"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            ""
          ]
        },
        "create_time": 1763709080.9044166,
        "end_turn": null,
        "id": "acb17a99-2de5-4ef7-8332-3c950369d371",
        "metadata": {
          "can_save": false,
          "classifier_response": "default",
          "debug_sonic_thread_id": "thread_69201098ec60832d8eaee17daa4b481c",
          "default_model_slug": "gpt-5-1-thinking",
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "ade81f7b-8e8b-4221-9e72-200c4788eba5",
          "reasoning_status": "is_reasoning",
          "request_id": "68f6df39-6ff0-4267-a5bc-79b130c89c99",
          "search_result_groups": [
            {
              "domain": "coinmarketcap.com",
              "entries": [
                {
                  "attribution": "coinmarketcap.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 0,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "PayPal USD is down 0.02% in the last 24 hours. The current CoinMarketCap ranking is #29, with a live market cap of $3,610,397,754 USD. It has a circulating ...",
                  "title": "PayPal USD price PYUSD #29",
                  "type": "search_result",
                  "url": "https://coinmarketcap.com/currencies/paypal-usd/"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "www.coinbase.com",
              "entries": [
                {
                  "attribution": "www.coinbase.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 1,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "PayPal USD (PYUSD) Price USD Today is $1.00. News, predictions, charts, market cap, buy, sell, convert, and invest on the most trusted platform for crypto.",
                  "title": "PayPal USD Price, PYUSD Price, Live Charts, and Marketcap",
                  "type": "search_result",
                  "url": "https://www.coinbase.com/price/paypal-usd"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "messari.io",
              "entries": [
                {
                  "attribution": "messari.io",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 2,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "PayPal USD (PYUSD) saw a significant 22% increase in its market capitalization over the past week, adding $600 million to its circulating supply 1.",
                  "title": "PayPal USD Price, PYUSD to USD, Research, News & ...",
                  "type": "search_result",
                  "url": "https://messari.io/project/pyusd"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "www.okx.com",
              "entries": [
                {
                  "attribution": "www.okx.com",
                  "pub_date": 1759055420.42,
                  "ref_id": {
                    "ref_index": 3,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "Sep 28, 2025 — With its market capitalization surging from $498 million to $1 billion in 2025, PYUSD is gaining traction among retail users, institutions, and ...",
                  "title": "PYUSD Market Growth: How PayPal's Stablecoin is ...",
                  "type": "search_result",
                  "url": "https://www.okx.com/learn/pyusd-market-growth-paypal-stablecoin"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "finance.yahoo.com",
              "entries": [
                {
                  "attribution": "finance.yahoo.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 4,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "Oct 4, 2025 — PayPal's PYUSD Stablecoin Tops $1 Billion Market Cap After Spark Partnership · What The Partnership Means · How PayPal Benefits From Its ...",
                  "title": "PayPal's PYUSD Stablecoin Tops $1 Billion Market Cap ...",
                  "type": "search_result",
                  "url": "https://finance.yahoo.com/news/paypals-pyusd-stablecoin-tops-1-154543932.html"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "www.paypal.com",
              "entries": [
                {
                  "attribution": "www.paypal.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 5,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "PYUSD is a stablecoin pegged 1:1 to USD, backed by US dollar deposits, and can be bought/sold on PayPal. Holding it may earn rewards.",
                  "title": "PYUSD Stablecoin | US Dollar Crypto Rewards",
                  "type": "search_result",
                  "url": "https://www.paypal.com/us/digital-wallet/manage-money/crypto/pyusd"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "www.gate.com",
              "entries": [
                {
                  "attribution": "www.gate.com",
                  "pub_date": 1763123504,
                  "ref_id": {
                    "ref_index": 6,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "7 days ago — As of 2025, PYUSD's market capitalization has reached $3.41 billion, with a circulating supply of approximately 3,408,934,195 tokens, ...",
                  "title": "2025 PYUSD Price Prediction: Analyzing Potential Growth ...",
                  "type": "search_result",
                  "url": "https://www.gate.com/crypto-wiki/article/2025-pyusd-price-prediction-analyzing-potential-growth-and-market-trends-for-the-emerging-stablecoin-20251114"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "www.coingecko.com",
              "entries": [
                {
                  "attribution": "www.coingecko.com",
                  "pub_date": 1758621049,
                  "ref_id": {
                    "ref_index": 7,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "Sep 24, 2025 — PYUSD joins a stablecoin market that has grown to almost $300 billion in total value, with these digital dollars becoming essential ...",
                  "title": "What Is PayPal USD (PYUSD)? Complete Guide to ...",
                  "type": "search_result",
                  "url": "https://www.coingecko.com/learn/what-is-paypal-usd-pyusd"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "www.mexc.com",
              "entries": [
                {
                  "attribution": "www.mexc.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 8,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "PYUSD's rapid growth is attributed to PayPal's extensive user base and its strong influence in the fintech industry. What does a $1 billion market cap mean in ...",
                  "title": "PYUSD Market Cap Exceeds $1 Billion: Will It Ignite the ...",
                  "type": "search_result",
                  "url": "https://www.mexc.com/learn/article/pyusd-market-cap-exceeds-1-billion-will-it-ignite-the-crypto-market-/1"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "www.kraken.com",
              "entries": [
                {
                  "attribution": "www.kraken.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 9,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "The circulating supply of PayPal USD is 3,611,904,340 PYUSD and the current PayPal USD market cap is $3,611,904,340. 114,427,378 PYUSD was purchased today on ...",
                  "title": "PayPal USD price today - PYUSD price chart & live trends",
                  "type": "search_result",
                  "url": "https://www.kraken.com/prices/paypal-usd"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "arxiv.org",
              "entries": [
                {
                  "attribution": "arxiv.org",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 10,
                    "ref_type": "academia",
                    "turn_index": 0
                  },
                  "snippet": "",
                  "title": "The Stablecoin Discount: Evidence of Tether's U.S. Treasury Bill Market Share in Lowering Yields",
                  "type": "search_result",
                  "url": "https://arxiv.org/abs/2505.12413"
                },
                {
                  "attribution": "arxiv.org",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 11,
                    "ref_type": "academia",
                    "turn_index": 0
                  },
                  "snippet": "",
                  "title": "SoK: Stablecoins for Digital Transformation -- Design, Metrics, and Application with Real World Asset Tokenization as a Case Study",
                  "type": "search_result",
                  "url": "https://arxiv.org/abs/2508.02403"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "de.wikipedia.org",
              "entries": [
                {
                  "attribution": "de.wikipedia.org",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 12,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "",
                  "title": "Stablecoin",
                  "type": "search_result",
                  "url": "https://de.wikipedia.org/wiki/Stablecoin"
                }
              ],
              "type": "search_result_group"
            }
          ],
          "timestamp_": "absolute",
          "turn_exchange_id": "9341c883-9f35-49b7-86b4-214248540d60"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "ade81f7b-8e8b-4221-9e72-200c4788eba5"
    },
    "ade81f7b-8e8b-4221-9e72-200c4788eba5": {
      "children": [
        "acb17a99-2de5-4ef7-8332-3c950369d371"
      ],
      "id": "ade81f7b-8e8b-4221-9e72-200c4788eba5",
      "message": {
        "author": {
          "metadata": {
            "real_author": "tool:web.run"
          },
          "name": "web.run",
          "role": "tool"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            ""
          ]
        },
        "create_time": 1763709080.9061356,
        "end_turn": null,
        "id": "ade81f7b-8e8b-4221-9e72-200c4788eba5",
        "metadata": {
          "can_save": false,
          "classifier_response": "default",
          "default_model_slug": "gpt-5-1-thinking",
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "35ab83de-73f6-4fdb-bb0e-026cf57ad7a5",
          "reasoning_status": "is_reasoning",
          "request_id": "68f6df39-6ff0-4267-a5bc-79b130c89c99",
          "search_model_queries": {
            "queries": [
              "PayPal USD stablecoin PYUSD market cap adoption"
            ],
            "type": "search_model_queries"
          },
          "timestamp_": "absolute",
          "turn_exchange_id": "9341c883-9f35-49b7-86b4-214248540d60"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "35ab83de-73f6-4fdb-bb0e-026cf57ad7a5"
    },
    "b3c87858-0de3-48a8-82bb-3b0eefeed442": {
      "children": [
        "9163c036-1689-4466-8ae9-14086a4f7751"
      ],
      "id": "b3c87858-0de3-48a8-82bb-3b0eefeed442",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "system"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            ""
          ]
        },
        "create_time": null,
        "end_turn": true,
        "id": "b3c87858-0de3-48a8-82bb-3b0eefeed442",
        "metadata": {
          "can_save": false,
          "is_visually_hidden_from_conversation": true,
          "rebase_developer_message": true
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 0
      },
      "parent": "0ca56f04-7635-4d51-9f12-828731bfd1a9"
    },
    "b4f8bbb2-b834-4ee6-9bfc-76df7002124f": {
      "children": [
        "27d4d82c-18a0-4b77-bc3f-741c36aba766"
      ],
      "id": "b4f8bbb2-b834-4ee6-9bfc-76df7002124f",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": "final",
        "content": {
          "content_type": "text",
          "parts": [
            "Right now, PYUSD is already a lot bigger than most people realize, but it’s not “USDT big” and probably won’t be anytime soon.\n\nfinanceturn0finance0  \n\n### Where PYUSD is today\n\n- Price: basically $1.00 (it’s a dollar-pegged stablecoin). citeturn0finance0  \n- Market cap: ~**$3.6B** and climbing, which puts it around the **top-30** of all crypto assets and in the upper tier of stablecoins. citeturn0search0turn0search1  \n- Growth: it’s been one of the fastest-growing stablecoins this year, with jumps of 20%+ in supply over short periods as PayPal pushes it, especially on Ethereum and Solana. citeturn0search2turn0search8  \n- PayPal angle: backed 1:1 by USD and Treasuries, usable directly in PayPal/Venmo, and they’re dangling around **4% rewards** for holding it inside PayPal. citeturn0search5  \n\nThe overall stablecoin market is around **$230–300B** now, dominated by USDT and USDC. citeturn0academia11turn0search12  \n\n### “How big can it get?” – realistic ranges\n\nObviously this is **speculation, not financial advice**, but here’s the no-nonsense view.\n\n#### 1) Boring / Bear-ish case  \nRegulators clamp harder, DeFi doesn’t really care about PYUSD, and it stays mostly a PayPal internal thing.\n\n- Range: maybe **$3–7B** market cap over the next few years.  \n- That’s enough to be a solid niche stablecoin, but not a major macro player.\n\n#### 2) Plausible / Base case (what I’d bet on)  \nPayPal keeps pushing PYUSD as the default “PayPal dollar” and wires it deeper into:\n\n- PayPal + Venmo P2P flows  \n- Merchant checkout  \n- A bit of DeFi and CEX liquidity  \n\nIn that world, PYUSD becomes the “PayPal house stablecoin” with some external usage.\n\n- Range: **$10–20B** market cap is very achievable over a multi-year horizon if adoption keeps compounding.  \n- That’d put it **below USDT/USDC but clearly in the top 3–5 stablecoins** if current leaders don’t explode in size again.\n\n#### 3) Aggressive / Bull case (everything lines up)  \nThis would need:\n\n- Strong US stablecoin regulation that explicitly favors big, regulated brands. citeturn0academia11  \n- PayPal really committing to on-chain rails (remittances, B2B payments, e-commerce settlement).  \n- Heavy integration in DeFi + CEXs + maybe tokenized T-bills and RWAs.\n\nThen you could talk about:\n\n- **$30–50B+** market cap territory, where PYUSD is sitting near USDC’s current scale and is a serious pillar of the stablecoin system.\n\nIs that possible? Yes.  \nIs it the most likely outcome? No. PayPal historically moves slower than “degen crypto,” and Tether/USDC have a big head start.\n\n### Blunt summary\n\n- PYUSD is already a multi-billion-dollar, top-tier stablecoin.  \n- Most reasonable ceiling in the near/mid-term: **mid-tier giant** (say, 10–20B), not “Tether killer.”  \n- Upside is tied less to price (it’s a stablecoin) and more to **how much of PayPal’s volume and DeFi liquidity migrates onto it**.\n\nIf you tell me what you’re really thinking (holding for yield, trading, farming, long-term thesis, etc.), I can walk through the actual risk/reward angle instead of just the size question."
          ]
        },
        "create_time": 1763709097.776333,
        "end_turn": true,
        "id": "b4f8bbb2-b834-4ee6-9bfc-76df7002124f",
        "metadata": {
          "can_save": true,
          "citations": [],
          "content_references": [
            {
              "alt": "## Stock market information for PayPal USD (PYUSD)\n- PayPal USD is a crypto in the CRYPTO market.\n- The price is 0.999341 USD currently with a change of -0.00 USD (-0.00%) from the previous close.\n- The intraday high is 1.001 USD and the intraday low is 0.998303 USD.\n",
              "asset_type": "crypto",
              "end_idx": 151,
              "market": "CRYPTO",
              "matched_text": "financeturn0finance0",
              "prompt_text": "PayPal USD (PYUSD) is a crypto in the CRYPTO market. The price is 0.999341 USD currently with a change of -0.00035 (-0.00035%) from the previous close. The intraday high is 1.001 USD and the intraday low is 0.998303 USD.",
              "refs": [
                {
                  "ref_index": 0,
                  "ref_type": "finance",
                  "turn_index": 0
                }
              ],
              "safe_urls": [],
              "start_idx": 128,
              "status": "done",
              "stock": {
                "asset": {
                  "asset_type": "crypto",
                  "latest_trading_period": {
                    "after_hours": null,
                    "pre_market": null,
                    "regular": {
                      "end_timestamp": 1763766000,
                      "end_utc_offset_sec": 0,
                      "start_timestamp": 1763683200,
                      "start_utc_offset_sec": 0
                    }
                  },
                  "market": "CRYPTO",
                  "name": "PayPal USD",
                  "ticker": "PYUSD",
                  "timezone": "UTC"
                },
                "histories": {
                  "quotes": {
                    "1d": [
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999508,
                        "timestamp": 1763679600
                      },
                      {
                        "close": 0.999995,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999645,
                        "timestamp": 1763679900
                      },
                      {
                        "close": 0.999781,
                        "currency_code": "USD",
                        "high": 0.99994,
                        "low": 0.999781,
                        "timestamp": 1763680200
                      },
                      {
                        "close": 0.999596,
                        "currency_code": "USD",
                        "high": 0.999967,
                        "low": 0.999285,
                        "timestamp": 1763680500
                      },
                      {
                        "close": 0.999389,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999389,
                        "timestamp": 1763680800
                      },
                      {
                        "close": 0.999819,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999691,
                        "timestamp": 1763681100
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999856,
                        "timestamp": 1763681400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999529,
                        "timestamp": 1763681700
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999534,
                        "timestamp": 1763682000
                      },
                      {
                        "close": 0.999602,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999602,
                        "timestamp": 1763682300
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999806,
                        "timestamp": 1763682600
                      },
                      {
                        "close": 0.99998,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999535,
                        "timestamp": 1763682900
                      },
                      {
                        "close": 0.999966,
                        "currency_code": "USD",
                        "high": 0.999967,
                        "low": 0.9998,
                        "timestamp": 1763683200
                      },
                      {
                        "close": 0.999915,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999241,
                        "timestamp": 1763683500
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999428,
                        "timestamp": 1763683800
                      },
                      {
                        "close": 0.999292,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999292,
                        "timestamp": 1763684100
                      },
                      {
                        "close": 0.999332,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999332,
                        "timestamp": 1763684400
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999709,
                        "timestamp": 1763684700
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99978,
                        "timestamp": 1763685000
                      },
                      {
                        "close": 0.999103,
                        "currency_code": "USD",
                        "high": 0.999711,
                        "low": 0.999103,
                        "timestamp": 1763685300
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999542,
                        "timestamp": 1763685600
                      },
                      {
                        "close": 0.999783,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999489,
                        "timestamp": 1763685900
                      },
                      {
                        "close": 0.999844,
                        "currency_code": "USD",
                        "high": 0.99989,
                        "low": 0.999521,
                        "timestamp": 1763686200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.9998,
                        "timestamp": 1763686500
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999466,
                        "timestamp": 1763686800
                      },
                      {
                        "close": 0.999956,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999577,
                        "timestamp": 1763687100
                      },
                      {
                        "close": 0.999955,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999819,
                        "timestamp": 1763687400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999786,
                        "timestamp": 1763687700
                      },
                      {
                        "close": 0.998833,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998833,
                        "timestamp": 1763688000
                      },
                      {
                        "close": 0.999902,
                        "currency_code": "USD",
                        "high": 0.999902,
                        "low": 0.999324,
                        "timestamp": 1763688300
                      },
                      {
                        "close": 0.999774,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999762,
                        "timestamp": 1763688600
                      },
                      {
                        "close": 0.99966,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99966,
                        "timestamp": 1763688900
                      },
                      {
                        "close": 0.999901,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999493,
                        "timestamp": 1763689200
                      },
                      {
                        "close": 0.999847,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999686,
                        "timestamp": 1763689500
                      },
                      {
                        "close": 0.999448,
                        "currency_code": "USD",
                        "high": 0.999472,
                        "low": 0.998795,
                        "timestamp": 1763689800
                      },
                      {
                        "close": 0.998832,
                        "currency_code": "USD",
                        "high": 0.999952,
                        "low": 0.998832,
                        "timestamp": 1763690100
                      },
                      {
                        "close": 0.99933,
                        "currency_code": "USD",
                        "high": 0.999536,
                        "low": 0.999188,
                        "timestamp": 1763690400
                      },
                      {
                        "close": 0.998974,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998974,
                        "timestamp": 1763690700
                      },
                      {
                        "close": 0.999574,
                        "currency_code": "USD",
                        "high": 0.999868,
                        "low": 0.999395,
                        "timestamp": 1763691000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999296,
                        "timestamp": 1763691300
                      },
                      {
                        "close": 0.999228,
                        "currency_code": "USD",
                        "high": 0.999765,
                        "low": 0.998849,
                        "timestamp": 1763691600
                      },
                      {
                        "close": 0.999879,
                        "currency_code": "USD",
                        "high": 0.999879,
                        "low": 0.999269,
                        "timestamp": 1763691900
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998303,
                        "timestamp": 1763692200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999019,
                        "timestamp": 1763692500
                      },
                      {
                        "close": 0.999448,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998809,
                        "timestamp": 1763692800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999259,
                        "timestamp": 1763693100
                      },
                      {
                        "close": 0.999562,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999444,
                        "timestamp": 1763693400
                      },
                      {
                        "close": 0.999998,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999524,
                        "timestamp": 1763693700
                      },
                      {
                        "close": 0.999664,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999412,
                        "timestamp": 1763694000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998634,
                        "timestamp": 1763694300
                      },
                      {
                        "close": 0.999478,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999478,
                        "timestamp": 1763694600
                      },
                      {
                        "close": 0.999282,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99918,
                        "timestamp": 1763694900
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999105,
                        "timestamp": 1763695200
                      },
                      {
                        "close": 0.999061,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999061,
                        "timestamp": 1763695500
                      },
                      {
                        "close": 0.999506,
                        "currency_code": "USD",
                        "high": 0.999506,
                        "low": 0.999427,
                        "timestamp": 1763695800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999462,
                        "timestamp": 1763696100
                      },
                      {
                        "close": 0.99961,
                        "currency_code": "USD",
                        "high": 0.99961,
                        "low": 0.99913,
                        "timestamp": 1763696400
                      },
                      {
                        "close": 0.999992,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999685,
                        "timestamp": 1763696700
                      },
                      {
                        "close": 0.999421,
                        "currency_code": "USD",
                        "high": 0.999836,
                        "low": 0.999155,
                        "timestamp": 1763697000
                      },
                      {
                        "close": 0.999195,
                        "currency_code": "USD",
                        "high": 0.999922,
                        "low": 0.999175,
                        "timestamp": 1763697300
                      },
                      {
                        "close": 0.999276,
                        "currency_code": "USD",
                        "high": 0.999857,
                        "low": 0.999259,
                        "timestamp": 1763697600
                      },
                      {
                        "close": 0.999472,
                        "currency_code": "USD",
                        "high": 0.999966,
                        "low": 0.999056,
                        "timestamp": 1763697900
                      },
                      {
                        "close": 0.999871,
                        "currency_code": "USD",
                        "high": 0.999871,
                        "low": 0.998956,
                        "timestamp": 1763698200
                      },
                      {
                        "close": 0.999882,
                        "currency_code": "USD",
                        "high": 0.999882,
                        "low": 0.999101,
                        "timestamp": 1763698500
                      },
                      {
                        "close": 0.999103,
                        "currency_code": "USD",
                        "high": 0.999851,
                        "low": 0.999103,
                        "timestamp": 1763698800
                      },
                      {
                        "close": 0.999142,
                        "currency_code": "USD",
                        "high": 0.999775,
                        "low": 0.99909,
                        "timestamp": 1763699100
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999171,
                        "timestamp": 1763699400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999028,
                        "timestamp": 1763699700
                      },
                      {
                        "close": 0.998812,
                        "currency_code": "USD",
                        "high": 0.999984,
                        "low": 0.998812,
                        "timestamp": 1763700000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999746,
                        "timestamp": 1763700300
                      },
                      {
                        "close": 0.999279,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999182,
                        "timestamp": 1763700600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99932,
                        "timestamp": 1763700900
                      },
                      {
                        "close": 0.999446,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999432,
                        "timestamp": 1763701200
                      },
                      {
                        "close": 0.999602,
                        "currency_code": "USD",
                        "high": 0.999703,
                        "low": 0.998593,
                        "timestamp": 1763701500
                      },
                      {
                        "close": 0.999178,
                        "currency_code": "USD",
                        "high": 0.999462,
                        "low": 0.998931,
                        "timestamp": 1763701800
                      },
                      {
                        "close": 0.999454,
                        "currency_code": "USD",
                        "high": 0.999517,
                        "low": 0.999055,
                        "timestamp": 1763702100
                      },
                      {
                        "close": 0.999708,
                        "currency_code": "USD",
                        "high": 0.999936,
                        "low": 0.999708,
                        "timestamp": 1763702400
                      },
                      {
                        "close": 0.999679,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999612,
                        "timestamp": 1763702700
                      },
                      {
                        "close": 0.999234,
                        "currency_code": "USD",
                        "high": 0.999518,
                        "low": 0.999138,
                        "timestamp": 1763703000
                      },
                      {
                        "close": 0.999258,
                        "currency_code": "USD",
                        "high": 0.999751,
                        "low": 0.999258,
                        "timestamp": 1763703300
                      },
                      {
                        "close": 0.99987,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99987,
                        "timestamp": 1763703600
                      },
                      {
                        "close": 0.999426,
                        "currency_code": "USD",
                        "high": 0.999772,
                        "low": 0.999083,
                        "timestamp": 1763703900
                      },
                      {
                        "close": 0.999776,
                        "currency_code": "USD",
                        "high": 0.999776,
                        "low": 0.999235,
                        "timestamp": 1763704200
                      },
                      {
                        "close": 0.999286,
                        "currency_code": "USD",
                        "high": 0.999843,
                        "low": 0.999277,
                        "timestamp": 1763704500
                      },
                      {
                        "close": 0.999383,
                        "currency_code": "USD",
                        "high": 0.999552,
                        "low": 0.999334,
                        "timestamp": 1763704800
                      },
                      {
                        "close": 0.999506,
                        "currency_code": "USD",
                        "high": 0.999839,
                        "low": 0.99891,
                        "timestamp": 1763705100
                      },
                      {
                        "close": 0.998518,
                        "currency_code": "USD",
                        "high": 0.999484,
                        "low": 0.998518,
                        "timestamp": 1763705400
                      },
                      {
                        "close": 0.999158,
                        "currency_code": "USD",
                        "high": 0.999545,
                        "low": 0.999158,
                        "timestamp": 1763705700
                      },
                      {
                        "close": 0.999639,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99955,
                        "timestamp": 1763706000
                      },
                      {
                        "close": 0.999637,
                        "currency_code": "USD",
                        "high": 0.9999,
                        "low": 0.999199,
                        "timestamp": 1763706300
                      },
                      {
                        "close": 0.999307,
                        "currency_code": "USD",
                        "high": 0.999715,
                        "low": 0.999259,
                        "timestamp": 1763706600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999155,
                        "timestamp": 1763706900
                      },
                      {
                        "close": 0.999433,
                        "currency_code": "USD",
                        "high": 0.999827,
                        "low": 0.998675,
                        "timestamp": 1763707200
                      },
                      {
                        "close": 0.999138,
                        "currency_code": "USD",
                        "high": 0.999825,
                        "low": 0.999138,
                        "timestamp": 1763707500
                      },
                      {
                        "close": 0.999671,
                        "currency_code": "USD",
                        "high": 0.999671,
                        "low": 0.999457,
                        "timestamp": 1763707800
                      },
                      {
                        "close": 0.9995,
                        "currency_code": "USD",
                        "high": 0.999774,
                        "low": 0.999188,
                        "timestamp": 1763708100
                      },
                      {
                        "close": 0.999426,
                        "currency_code": "USD",
                        "high": 0.999426,
                        "low": 0.999289,
                        "timestamp": 1763708400
                      },
                      {
                        "close": 0.999751,
                        "currency_code": "USD",
                        "high": 0.999751,
                        "low": 0.999128,
                        "timestamp": 1763708700
                      },
                      {
                        "close": 0.999341,
                        "currency_code": "USD",
                        "high": 0.999379,
                        "low": 0.999341,
                        "timestamp": 1763709000
                      }
                    ],
                    "1m": [
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99923,
                        "timestamp": 1761091200
                      },
                      {
                        "close": 0.9999,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999364,
                        "timestamp": 1761177600
                      },
                      {
                        "close": 0.999947,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999127,
                        "timestamp": 1761264000
                      },
                      {
                        "close": 0.999872,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999299,
                        "timestamp": 1761350400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999524,
                        "timestamp": 1761436800
                      },
                      {
                        "close": 0.999962,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999389,
                        "timestamp": 1761523200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999103,
                        "timestamp": 1761609600
                      },
                      {
                        "close": 0.999957,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99874,
                        "timestamp": 1761696000
                      },
                      {
                        "close": 0.999724,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999012,
                        "timestamp": 1761782400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998979,
                        "timestamp": 1761868800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999334,
                        "timestamp": 1761955200
                      },
                      {
                        "close": 0.999953,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99945,
                        "timestamp": 1762041600
                      },
                      {
                        "close": 0.999845,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998958,
                        "timestamp": 1762128000
                      },
                      {
                        "close": 0.999749,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998511,
                        "timestamp": 1762214400
                      },
                      {
                        "close": 0.999653,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999064,
                        "timestamp": 1762300800
                      },
                      {
                        "close": 0.999621,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998328,
                        "timestamp": 1762387200
                      },
                      {
                        "close": 0.999863,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999015,
                        "timestamp": 1762473600
                      },
                      {
                        "close": 0.999961,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999452,
                        "timestamp": 1762560000
                      },
                      {
                        "close": 0.999754,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99924,
                        "timestamp": 1762646400
                      },
                      {
                        "close": 0.999391,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999242,
                        "timestamp": 1762732800
                      },
                      {
                        "close": 0.999726,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999159,
                        "timestamp": 1762819200
                      },
                      {
                        "close": 0.999418,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998937,
                        "timestamp": 1762905600
                      },
                      {
                        "close": 0.999937,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998893,
                        "timestamp": 1762992000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998596,
                        "timestamp": 1763078400
                      },
                      {
                        "close": 0.999921,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999132,
                        "timestamp": 1763164800
                      },
                      {
                        "close": 0.99985,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998893,
                        "timestamp": 1763251200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998753,
                        "timestamp": 1763337600
                      },
                      {
                        "close": 0.999973,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998451,
                        "timestamp": 1763424000
                      },
                      {
                        "close": 0.999529,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999168,
                        "timestamp": 1763510400
                      },
                      {
                        "close": 0.999601,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998835,
                        "timestamp": 1763596800
                      }
                    ],
                    "1y": [
                      {
                        "close": 0.999903,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.995175,
                        "timestamp": 1732233600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997455,
                        "timestamp": 1732320000
                      },
                      {
                        "close": 0.999804,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.996514,
                        "timestamp": 1732406400
                      },
                      {
                        "close": 0.99946,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.993754,
                        "timestamp": 1732492800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.01,
                        "low": 0.993308,
                        "timestamp": 1732579200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.99702,
                        "timestamp": 1732665600
                      },
                      {
                        "close": 0.999305,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.996827,
                        "timestamp": 1732752000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.996367,
                        "timestamp": 1732838400
                      },
                      {
                        "close": 0.999443,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.997893,
                        "timestamp": 1732924800
                      },
                      {
                        "close": 0.999147,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997479,
                        "timestamp": 1733011200
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.993249,
                        "timestamp": 1733097600
                      },
                      {
                        "close": 0.999652,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.995332,
                        "timestamp": 1733184000
                      },
                      {
                        "close": 0.999455,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.995889,
                        "timestamp": 1733270400
                      },
                      {
                        "close": 1.002,
                        "currency_code": "USD",
                        "high": 1.009,
                        "low": 0.959426,
                        "timestamp": 1733356800
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.994581,
                        "timestamp": 1733443200
                      },
                      {
                        "close": 0.99901,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.997827,
                        "timestamp": 1733529600
                      },
                      {
                        "close": 1.002,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.998012,
                        "timestamp": 1733616000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.989632,
                        "timestamp": 1733702400
                      },
                      {
                        "close": 0.999555,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.994623,
                        "timestamp": 1733788800
                      },
                      {
                        "close": 0.999545,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.995754,
                        "timestamp": 1733875200
                      },
                      {
                        "close": 0.999483,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.994917,
                        "timestamp": 1733961600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.995641,
                        "timestamp": 1734048000
                      },
                      {
                        "close": 0.999827,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.997339,
                        "timestamp": 1734134400
                      },
                      {
                        "close": 0.999542,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.997865,
                        "timestamp": 1734220800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.996451,
                        "timestamp": 1734307200
                      },
                      {
                        "close": 0.999543,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.996049,
                        "timestamp": 1734393600
                      },
                      {
                        "close": 0.99965,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.995349,
                        "timestamp": 1734480000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.009,
                        "low": 0.995049,
                        "timestamp": 1734566400
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.99482,
                        "timestamp": 1734652800
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.996317,
                        "timestamp": 1734739200
                      },
                      {
                        "close": 0.999123,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.996113,
                        "timestamp": 1734825600
                      },
                      {
                        "close": 0.999624,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.995653,
                        "timestamp": 1734912000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.996613,
                        "timestamp": 1734998400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.997718,
                        "timestamp": 1735084800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.992025,
                        "timestamp": 1735171200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.9938,
                        "timestamp": 1735257600
                      },
                      {
                        "close": 0.999786,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.997373,
                        "timestamp": 1735344000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.99711,
                        "timestamp": 1735430400
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.995057,
                        "timestamp": 1735516800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.99449,
                        "timestamp": 1735603200
                      },
                      {
                        "close": 0.999294,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.997396,
                        "timestamp": 1735689600
                      },
                      {
                        "close": 0.999743,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.996306,
                        "timestamp": 1735776000
                      },
                      {
                        "close": 0.999683,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.997661,
                        "timestamp": 1735862400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997077,
                        "timestamp": 1735948800
                      },
                      {
                        "close": 0.999837,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.998013,
                        "timestamp": 1736035200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.995804,
                        "timestamp": 1736121600
                      },
                      {
                        "close": 0.999857,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.993702,
                        "timestamp": 1736208000
                      },
                      {
                        "close": 0.999486,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.995348,
                        "timestamp": 1736294400
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.99184,
                        "timestamp": 1736380800
                      },
                      {
                        "close": 0.99986,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.992508,
                        "timestamp": 1736467200
                      },
                      {
                        "close": 0.999537,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.99794,
                        "timestamp": 1736553600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997628,
                        "timestamp": 1736640000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.014,
                        "low": 0.992923,
                        "timestamp": 1736726400
                      },
                      {
                        "close": 0.999961,
                        "currency_code": "USD",
                        "high": 1.008,
                        "low": 0.99494,
                        "timestamp": 1736812800
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.996924,
                        "timestamp": 1736899200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.993447,
                        "timestamp": 1736985600
                      },
                      {
                        "close": 0.999777,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.995588,
                        "timestamp": 1737072000
                      },
                      {
                        "close": 0.999674,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.994448,
                        "timestamp": 1737158400
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.008,
                        "low": 0.98469,
                        "timestamp": 1737244800
                      },
                      {
                        "close": 0.998593,
                        "currency_code": "USD",
                        "high": 1.016,
                        "low": 0.978146,
                        "timestamp": 1737331200
                      },
                      {
                        "close": 1.002,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.993054,
                        "timestamp": 1737417600
                      },
                      {
                        "close": 0.999368,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.99725,
                        "timestamp": 1737504000
                      },
                      {
                        "close": 0.999089,
                        "currency_code": "USD",
                        "high": 1.011,
                        "low": 0.987658,
                        "timestamp": 1737590400
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.997098,
                        "timestamp": 1737676800
                      },
                      {
                        "close": 0.999744,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998861,
                        "timestamp": 1737763200
                      },
                      {
                        "close": 0.998347,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.997491,
                        "timestamp": 1737849600
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.994705,
                        "timestamp": 1737936000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.996743,
                        "timestamp": 1738022400
                      },
                      {
                        "close": 0.999447,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.995221,
                        "timestamp": 1738108800
                      },
                      {
                        "close": 0.998796,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.996861,
                        "timestamp": 1738195200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.99633,
                        "timestamp": 1738281600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.996966,
                        "timestamp": 1738368000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.994198,
                        "timestamp": 1738454400
                      },
                      {
                        "close": 0.999403,
                        "currency_code": "USD",
                        "high": 1.008,
                        "low": 0.987048,
                        "timestamp": 1738540800
                      },
                      {
                        "close": 1.002,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.98999,
                        "timestamp": 1738627200
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.992324,
                        "timestamp": 1738713600
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.993846,
                        "timestamp": 1738800000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.993298,
                        "timestamp": 1738886400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998256,
                        "timestamp": 1738972800
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.996879,
                        "timestamp": 1739059200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.995701,
                        "timestamp": 1739145600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997373,
                        "timestamp": 1739232000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.993554,
                        "timestamp": 1739318400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.997647,
                        "timestamp": 1739404800
                      },
                      {
                        "close": 0.999957,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.996389,
                        "timestamp": 1739491200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998206,
                        "timestamp": 1739577600
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998816,
                        "timestamp": 1739664000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.996878,
                        "timestamp": 1739750400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.997258,
                        "timestamp": 1739836800
                      },
                      {
                        "close": 0.999451,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.996994,
                        "timestamp": 1739923200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.995987,
                        "timestamp": 1740009600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.99652,
                        "timestamp": 1740096000
                      },
                      {
                        "close": 0.999941,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.999136,
                        "timestamp": 1740182400
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998357,
                        "timestamp": 1740268800
                      },
                      {
                        "close": 0.999271,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.996668,
                        "timestamp": 1740355200
                      },
                      {
                        "close": 0.999425,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.993208,
                        "timestamp": 1740441600
                      },
                      {
                        "close": 0.999638,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99932,
                        "timestamp": 1740528000
                      },
                      {
                        "close": 0.999758,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998519,
                        "timestamp": 1740614400
                      },
                      {
                        "close": 0.999982,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998408,
                        "timestamp": 1740700800
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999147,
                        "timestamp": 1740787200
                      },
                      {
                        "close": 0.99893,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998625,
                        "timestamp": 1740873600
                      },
                      {
                        "close": 0.998805,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998172,
                        "timestamp": 1740960000
                      },
                      {
                        "close": 0.999498,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.997447,
                        "timestamp": 1741046400
                      },
                      {
                        "close": 0.999918,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998607,
                        "timestamp": 1741132800
                      },
                      {
                        "close": 0.998361,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998272,
                        "timestamp": 1741219200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997452,
                        "timestamp": 1741305600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998617,
                        "timestamp": 1741392000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998024,
                        "timestamp": 1741478400
                      },
                      {
                        "close": 0.99985,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997659,
                        "timestamp": 1741564800
                      },
                      {
                        "close": 0.999066,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998414,
                        "timestamp": 1741651200
                      },
                      {
                        "close": 0.999868,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998417,
                        "timestamp": 1741737600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997953,
                        "timestamp": 1741824000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998097,
                        "timestamp": 1741910400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998964,
                        "timestamp": 1741996800
                      },
                      {
                        "close": 0.999781,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998429,
                        "timestamp": 1742083200
                      },
                      {
                        "close": 0.999828,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998066,
                        "timestamp": 1742169600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.997346,
                        "timestamp": 1742256000
                      },
                      {
                        "close": 0.999498,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99863,
                        "timestamp": 1742342400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998733,
                        "timestamp": 1742428800
                      },
                      {
                        "close": 0.99973,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998958,
                        "timestamp": 1742515200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999396,
                        "timestamp": 1742601600
                      },
                      {
                        "close": 0.999562,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999287,
                        "timestamp": 1742688000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999165,
                        "timestamp": 1742774400
                      },
                      {
                        "close": 0.999688,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999107,
                        "timestamp": 1742860800
                      },
                      {
                        "close": 0.99992,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999136,
                        "timestamp": 1742947200
                      },
                      {
                        "close": 0.999581,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998507,
                        "timestamp": 1743033600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99854,
                        "timestamp": 1743120000
                      },
                      {
                        "close": 0.999981,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999175,
                        "timestamp": 1743206400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998713,
                        "timestamp": 1743292800
                      },
                      {
                        "close": 0.999669,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998649,
                        "timestamp": 1743379200
                      },
                      {
                        "close": 0.999453,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998751,
                        "timestamp": 1743465600
                      },
                      {
                        "close": 0.999858,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998626,
                        "timestamp": 1743552000
                      },
                      {
                        "close": 0.99956,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99863,
                        "timestamp": 1743638400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998658,
                        "timestamp": 1743724800
                      },
                      {
                        "close": 0.999794,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999122,
                        "timestamp": 1743811200
                      },
                      {
                        "close": 0.998962,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998276,
                        "timestamp": 1743897600
                      },
                      {
                        "close": 0.999908,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99872,
                        "timestamp": 1743984000
                      },
                      {
                        "close": 0.999812,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998408,
                        "timestamp": 1744070400
                      },
                      {
                        "close": 0.999382,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998534,
                        "timestamp": 1744156800
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998519,
                        "timestamp": 1744243200
                      },
                      {
                        "close": 0.999857,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998543,
                        "timestamp": 1744329600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998709,
                        "timestamp": 1744416000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998796,
                        "timestamp": 1744502400
                      },
                      {
                        "close": 0.999203,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998793,
                        "timestamp": 1744588800
                      },
                      {
                        "close": 0.999758,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999063,
                        "timestamp": 1744675200
                      },
                      {
                        "close": 0.999615,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999092,
                        "timestamp": 1744761600
                      },
                      {
                        "close": 0.999792,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998969,
                        "timestamp": 1744848000
                      },
                      {
                        "close": 0.999807,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999231,
                        "timestamp": 1744934400
                      },
                      {
                        "close": 0.999871,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999494,
                        "timestamp": 1745020800
                      },
                      {
                        "close": 0.999891,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999367,
                        "timestamp": 1745107200
                      },
                      {
                        "close": 0.999842,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999184,
                        "timestamp": 1745193600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999171,
                        "timestamp": 1745280000
                      },
                      {
                        "close": 0.99995,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999293,
                        "timestamp": 1745366400
                      },
                      {
                        "close": 0.999989,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999372,
                        "timestamp": 1745452800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999388,
                        "timestamp": 1745539200
                      },
                      {
                        "close": 0.999854,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999353,
                        "timestamp": 1745625600
                      },
                      {
                        "close": 0.99986,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999549,
                        "timestamp": 1745712000
                      },
                      {
                        "close": 0.999927,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999302,
                        "timestamp": 1745798400
                      },
                      {
                        "close": 0.999941,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999261,
                        "timestamp": 1745884800
                      },
                      {
                        "close": 0.999511,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99912,
                        "timestamp": 1745971200
                      },
                      {
                        "close": 0.999704,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999319,
                        "timestamp": 1746057600
                      },
                      {
                        "close": 0.999536,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999439,
                        "timestamp": 1746144000
                      },
                      {
                        "close": 0.999829,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999262,
                        "timestamp": 1746230400
                      },
                      {
                        "close": 0.99977,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999136,
                        "timestamp": 1746316800
                      },
                      {
                        "close": 0.999562,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999379,
                        "timestamp": 1746403200
                      },
                      {
                        "close": 0.999607,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999376,
                        "timestamp": 1746489600
                      },
                      {
                        "close": 0.999649,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999382,
                        "timestamp": 1746576000
                      },
                      {
                        "close": 0.999776,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999291,
                        "timestamp": 1746662400
                      },
                      {
                        "close": 0.999738,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999045,
                        "timestamp": 1746748800
                      },
                      {
                        "close": 0.999947,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999397,
                        "timestamp": 1746835200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999455,
                        "timestamp": 1746921600
                      },
                      {
                        "close": 0.999871,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999341,
                        "timestamp": 1747008000
                      },
                      {
                        "close": 0.99989,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999319,
                        "timestamp": 1747094400
                      },
                      {
                        "close": 0.999786,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999508,
                        "timestamp": 1747180800
                      },
                      {
                        "close": 0.999674,
                        "currency_code": "USD",
                        "high": 0.999992,
                        "low": 0.999323,
                        "timestamp": 1747267200
                      },
                      {
                        "close": 0.999699,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999241,
                        "timestamp": 1747353600
                      },
                      {
                        "close": 0.999633,
                        "currency_code": "USD",
                        "high": 0.999833,
                        "low": 0.999351,
                        "timestamp": 1747440000
                      },
                      {
                        "close": 0.999636,
                        "currency_code": "USD",
                        "high": 0.999792,
                        "low": 0.999481,
                        "timestamp": 1747526400
                      },
                      {
                        "close": 0.999709,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999227,
                        "timestamp": 1747612800
                      },
                      {
                        "close": 0.999584,
                        "currency_code": "USD",
                        "high": 0.999895,
                        "low": 0.99924,
                        "timestamp": 1747699200
                      },
                      {
                        "close": 0.99965,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999193,
                        "timestamp": 1747785600
                      },
                      {
                        "close": 0.999597,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998672,
                        "timestamp": 1747872000
                      },
                      {
                        "close": 0.999445,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998925,
                        "timestamp": 1747958400
                      },
                      {
                        "close": 0.999736,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998805,
                        "timestamp": 1748044800
                      },
                      {
                        "close": 0.999367,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99882,
                        "timestamp": 1748131200
                      },
                      {
                        "close": 0.999742,
                        "currency_code": "USD",
                        "high": 0.99986,
                        "low": 0.999043,
                        "timestamp": 1748217600
                      },
                      {
                        "close": 0.999515,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999007,
                        "timestamp": 1748304000
                      },
                      {
                        "close": 0.999731,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99919,
                        "timestamp": 1748390400
                      },
                      {
                        "close": 0.999341,
                        "currency_code": "USD",
                        "high": 0.999883,
                        "low": 0.999167,
                        "timestamp": 1748476800
                      },
                      {
                        "close": 0.999514,
                        "currency_code": "USD",
                        "high": 0.999885,
                        "low": 0.999255,
                        "timestamp": 1748563200
                      },
                      {
                        "close": 0.999325,
                        "currency_code": "USD",
                        "high": 0.999786,
                        "low": 0.999302,
                        "timestamp": 1748649600
                      },
                      {
                        "close": 0.999614,
                        "currency_code": "USD",
                        "high": 0.999793,
                        "low": 0.998824,
                        "timestamp": 1748736000
                      },
                      {
                        "close": 0.999626,
                        "currency_code": "USD",
                        "high": 0.999896,
                        "low": 0.998667,
                        "timestamp": 1748822400
                      },
                      {
                        "close": 0.999638,
                        "currency_code": "USD",
                        "high": 0.999807,
                        "low": 0.999306,
                        "timestamp": 1748908800
                      },
                      {
                        "close": 0.999636,
                        "currency_code": "USD",
                        "high": 0.999949,
                        "low": 0.999455,
                        "timestamp": 1748995200
                      },
                      {
                        "close": 0.999361,
                        "currency_code": "USD",
                        "high": 0.99998,
                        "low": 0.999205,
                        "timestamp": 1749081600
                      },
                      {
                        "close": 0.999188,
                        "currency_code": "USD",
                        "high": 0.999834,
                        "low": 0.998885,
                        "timestamp": 1749168000
                      },
                      {
                        "close": 0.999395,
                        "currency_code": "USD",
                        "high": 0.999756,
                        "low": 0.998669,
                        "timestamp": 1749254400
                      },
                      {
                        "close": 0.99988,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999235,
                        "timestamp": 1749340800
                      },
                      {
                        "close": 0.999446,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99922,
                        "timestamp": 1749427200
                      },
                      {
                        "close": 0.999294,
                        "currency_code": "USD",
                        "high": 0.999847,
                        "low": 0.999137,
                        "timestamp": 1749513600
                      },
                      {
                        "close": 0.999725,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999118,
                        "timestamp": 1749600000
                      },
                      {
                        "close": 0.999414,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99906,
                        "timestamp": 1749686400
                      },
                      {
                        "close": 0.999676,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998964,
                        "timestamp": 1749772800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999254,
                        "timestamp": 1749859200
                      },
                      {
                        "close": 0.999633,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999268,
                        "timestamp": 1749945600
                      },
                      {
                        "close": 0.998864,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998864,
                        "timestamp": 1750032000
                      },
                      {
                        "close": 0.999659,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999145,
                        "timestamp": 1750118400
                      },
                      {
                        "close": 0.999598,
                        "currency_code": "USD",
                        "high": 0.999979,
                        "low": 0.999267,
                        "timestamp": 1750204800
                      },
                      {
                        "close": 0.999444,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.9992,
                        "timestamp": 1750291200
                      },
                      {
                        "close": 0.999473,
                        "currency_code": "USD",
                        "high": 0.999953,
                        "low": 0.999109,
                        "timestamp": 1750377600
                      },
                      {
                        "close": 0.999644,
                        "currency_code": "USD",
                        "high": 0.999927,
                        "low": 0.999224,
                        "timestamp": 1750464000
                      },
                      {
                        "close": 0.999942,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999287,
                        "timestamp": 1750550400
                      },
                      {
                        "close": 0.999871,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998768,
                        "timestamp": 1750636800
                      },
                      {
                        "close": 0.99975,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99917,
                        "timestamp": 1750723200
                      },
                      {
                        "close": 0.999541,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998865,
                        "timestamp": 1750809600
                      },
                      {
                        "close": 0.999431,
                        "currency_code": "USD",
                        "high": 0.99991,
                        "low": 0.999345,
                        "timestamp": 1750896000
                      },
                      {
                        "close": 0.999504,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999182,
                        "timestamp": 1750982400
                      },
                      {
                        "close": 0.999757,
                        "currency_code": "USD",
                        "high": 0.999856,
                        "low": 0.999364,
                        "timestamp": 1751068800
                      },
                      {
                        "close": 0.999608,
                        "currency_code": "USD",
                        "high": 0.999865,
                        "low": 0.999283,
                        "timestamp": 1751155200
                      },
                      {
                        "close": 0.999878,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999173,
                        "timestamp": 1751241600
                      },
                      {
                        "close": 0.999541,
                        "currency_code": "USD",
                        "high": 0.999914,
                        "low": 0.999082,
                        "timestamp": 1751328000
                      },
                      {
                        "close": 0.999513,
                        "currency_code": "USD",
                        "high": 0.999971,
                        "low": 0.999373,
                        "timestamp": 1751414400
                      },
                      {
                        "close": 0.99979,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998993,
                        "timestamp": 1751500800
                      },
                      {
                        "close": 0.999849,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999399,
                        "timestamp": 1751587200
                      },
                      {
                        "close": 0.999735,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999354,
                        "timestamp": 1751673600
                      },
                      {
                        "close": 0.999606,
                        "currency_code": "USD",
                        "high": 0.999904,
                        "low": 0.999077,
                        "timestamp": 1751760000
                      },
                      {
                        "close": 0.999887,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998904,
                        "timestamp": 1751846400
                      },
                      {
                        "close": 0.9998,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999447,
                        "timestamp": 1751932800
                      },
                      {
                        "close": 0.999636,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998979,
                        "timestamp": 1752019200
                      },
                      {
                        "close": 0.999512,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999187,
                        "timestamp": 1752105600
                      },
                      {
                        "close": 0.999537,
                        "currency_code": "USD",
                        "high": 0.999945,
                        "low": 0.99905,
                        "timestamp": 1752192000
                      },
                      {
                        "close": 0.999581,
                        "currency_code": "USD",
                        "high": 0.999886,
                        "low": 0.999098,
                        "timestamp": 1752278400
                      },
                      {
                        "close": 0.999651,
                        "currency_code": "USD",
                        "high": 0.999773,
                        "low": 0.999141,
                        "timestamp": 1752364800
                      },
                      {
                        "close": 0.999694,
                        "currency_code": "USD",
                        "high": 0.999785,
                        "low": 0.998938,
                        "timestamp": 1752451200
                      },
                      {
                        "close": 0.999647,
                        "currency_code": "USD",
                        "high": 0.99996,
                        "low": 0.998674,
                        "timestamp": 1752537600
                      },
                      {
                        "close": 0.999773,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999115,
                        "timestamp": 1752624000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999152,
                        "timestamp": 1752710400
                      },
                      {
                        "close": 0.999678,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999431,
                        "timestamp": 1752796800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999597,
                        "timestamp": 1752883200
                      },
                      {
                        "close": 0.999532,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999223,
                        "timestamp": 1752969600
                      },
                      {
                        "close": 0.99965,
                        "currency_code": "USD",
                        "high": 0.99994,
                        "low": 0.99927,
                        "timestamp": 1753056000
                      },
                      {
                        "close": 0.999762,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.9995,
                        "timestamp": 1753142400
                      },
                      {
                        "close": 0.999745,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999279,
                        "timestamp": 1753228800
                      },
                      {
                        "close": 0.999351,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999302,
                        "timestamp": 1753315200
                      },
                      {
                        "close": 0.999906,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998862,
                        "timestamp": 1753401600
                      },
                      {
                        "close": 0.999759,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999341,
                        "timestamp": 1753488000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999234,
                        "timestamp": 1753574400
                      },
                      {
                        "close": 0.999935,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999058,
                        "timestamp": 1753660800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999073,
                        "timestamp": 1753747200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999035,
                        "timestamp": 1753833600
                      },
                      {
                        "close": 0.999331,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999041,
                        "timestamp": 1753920000
                      },
                      {
                        "close": 0.999742,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998673,
                        "timestamp": 1754006400
                      },
                      {
                        "close": 0.999513,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998953,
                        "timestamp": 1754092800
                      },
                      {
                        "close": 0.999652,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999081,
                        "timestamp": 1754179200
                      },
                      {
                        "close": 0.999372,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998819,
                        "timestamp": 1754265600
                      },
                      {
                        "close": 0.999867,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998779,
                        "timestamp": 1754352000
                      },
                      {
                        "close": 0.999742,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999058,
                        "timestamp": 1754438400
                      },
                      {
                        "close": 0.999908,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998825,
                        "timestamp": 1754524800
                      },
                      {
                        "close": 0.999777,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999011,
                        "timestamp": 1754611200
                      },
                      {
                        "close": 0.999611,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999235,
                        "timestamp": 1754697600
                      },
                      {
                        "close": 0.999598,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99895,
                        "timestamp": 1754784000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998937,
                        "timestamp": 1754870400
                      },
                      {
                        "close": 0.999705,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999029,
                        "timestamp": 1754956800
                      },
                      {
                        "close": 0.999506,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999129,
                        "timestamp": 1755043200
                      },
                      {
                        "close": 0.999782,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99919,
                        "timestamp": 1755129600
                      },
                      {
                        "close": 0.99976,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999279,
                        "timestamp": 1755216000
                      },
                      {
                        "close": 0.999932,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999546,
                        "timestamp": 1755302400
                      },
                      {
                        "close": 0.999958,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999562,
                        "timestamp": 1755388800
                      },
                      {
                        "close": 0.999863,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999513,
                        "timestamp": 1755475200
                      },
                      {
                        "close": 0.999872,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999591,
                        "timestamp": 1755561600
                      },
                      {
                        "close": 0.999845,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999379,
                        "timestamp": 1755648000
                      },
                      {
                        "close": 0.999484,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999302,
                        "timestamp": 1755734400
                      },
                      {
                        "close": 0.99963,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999121,
                        "timestamp": 1755820800
                      },
                      {
                        "close": 0.999578,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999216,
                        "timestamp": 1755907200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999247,
                        "timestamp": 1755993600
                      },
                      {
                        "close": 0.999783,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998956,
                        "timestamp": 1756080000
                      },
                      {
                        "close": 0.999906,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999215,
                        "timestamp": 1756166400
                      },
                      {
                        "close": 0.999837,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999131,
                        "timestamp": 1756252800
                      },
                      {
                        "close": 0.999465,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999072,
                        "timestamp": 1756339200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998987,
                        "timestamp": 1756425600
                      },
                      {
                        "close": 0.999448,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999349,
                        "timestamp": 1756512000
                      },
                      {
                        "close": 0.999408,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999248,
                        "timestamp": 1756598400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999212,
                        "timestamp": 1756684800
                      },
                      {
                        "close": 0.999702,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999196,
                        "timestamp": 1756771200
                      },
                      {
                        "close": 0.999858,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999277,
                        "timestamp": 1756857600
                      },
                      {
                        "close": 0.999709,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999229,
                        "timestamp": 1756944000
                      },
                      {
                        "close": 0.999724,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999132,
                        "timestamp": 1757030400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998964,
                        "timestamp": 1757116800
                      },
                      {
                        "close": 0.999965,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999444,
                        "timestamp": 1757203200
                      },
                      {
                        "close": 0.999804,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99921,
                        "timestamp": 1757289600
                      },
                      {
                        "close": 0.99985,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999349,
                        "timestamp": 1757376000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999157,
                        "timestamp": 1757462400
                      },
                      {
                        "close": 0.999871,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999017,
                        "timestamp": 1757548800
                      },
                      {
                        "close": 0.999924,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999302,
                        "timestamp": 1757635200
                      },
                      {
                        "close": 0.999793,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999428,
                        "timestamp": 1757721600
                      },
                      {
                        "close": 0.999763,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999603,
                        "timestamp": 1757808000
                      },
                      {
                        "close": 0.999843,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999357,
                        "timestamp": 1757894400
                      },
                      {
                        "close": 0.999837,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999452,
                        "timestamp": 1757980800
                      },
                      {
                        "close": 0.999759,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999174,
                        "timestamp": 1758067200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998666,
                        "timestamp": 1758153600
                      },
                      {
                        "close": 0.999878,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998049,
                        "timestamp": 1758240000
                      },
                      {
                        "close": 0.999783,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998635,
                        "timestamp": 1758326400
                      },
                      {
                        "close": 0.999783,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999345,
                        "timestamp": 1758412800
                      },
                      {
                        "close": 0.999736,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999073,
                        "timestamp": 1758499200
                      },
                      {
                        "close": 0.99988,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998516,
                        "timestamp": 1758585600
                      },
                      {
                        "close": 0.999861,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998455,
                        "timestamp": 1758672000
                      },
                      {
                        "close": 0.999899,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997671,
                        "timestamp": 1758758400
                      },
                      {
                        "close": 0.999737,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.997598,
                        "timestamp": 1758844800
                      },
                      {
                        "close": 0.99967,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.999386,
                        "timestamp": 1758931200
                      },
                      {
                        "close": 0.999996,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.999423,
                        "timestamp": 1759017600
                      },
                      {
                        "close": 0.999812,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.997591,
                        "timestamp": 1759104000
                      },
                      {
                        "close": 0.999759,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.997367,
                        "timestamp": 1759190400
                      },
                      {
                        "close": 0.999929,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99726,
                        "timestamp": 1759276800
                      },
                      {
                        "close": 0.999761,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999165,
                        "timestamp": 1759363200
                      },
                      {
                        "close": 0.999703,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999306,
                        "timestamp": 1759449600
                      },
                      {
                        "close": 0.999861,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999106,
                        "timestamp": 1759536000
                      },
                      {
                        "close": 0.999947,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998487,
                        "timestamp": 1759622400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999115,
                        "timestamp": 1759708800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999038,
                        "timestamp": 1759795200
                      },
                      {
                        "close": 0.999937,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998948,
                        "timestamp": 1759881600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999399,
                        "timestamp": 1759968000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998834,
                        "timestamp": 1760054400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998707,
                        "timestamp": 1760140800
                      },
                      {
                        "close": 0.999948,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999256,
                        "timestamp": 1760227200
                      },
                      {
                        "close": 0.999932,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999409,
                        "timestamp": 1760313600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999421,
                        "timestamp": 1760400000
                      },
                      {
                        "close": 0.999903,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999268,
                        "timestamp": 1760486400
                      },
                      {
                        "close": 0.999696,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999296,
                        "timestamp": 1760572800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999042,
                        "timestamp": 1760659200
                      },
                      {
                        "close": 0.999969,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.9993,
                        "timestamp": 1760745600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999427,
                        "timestamp": 1760832000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999327,
                        "timestamp": 1760918400
                      },
                      {
                        "close": 0.999815,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999049,
                        "timestamp": 1761004800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99923,
                        "timestamp": 1761091200
                      },
                      {
                        "close": 0.9999,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999364,
                        "timestamp": 1761177600
                      },
                      {
                        "close": 0.999947,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999127,
                        "timestamp": 1761264000
                      },
                      {
                        "close": 0.999872,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999299,
                        "timestamp": 1761350400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999524,
                        "timestamp": 1761436800
                      },
                      {
                        "close": 0.999962,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999389,
                        "timestamp": 1761523200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999103,
                        "timestamp": 1761609600
                      },
                      {
                        "close": 0.999957,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99874,
                        "timestamp": 1761696000
                      },
                      {
                        "close": 0.999724,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999012,
                        "timestamp": 1761782400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998979,
                        "timestamp": 1761868800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999334,
                        "timestamp": 1761955200
                      },
                      {
                        "close": 0.999953,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99945,
                        "timestamp": 1762041600
                      },
                      {
                        "close": 0.999845,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998958,
                        "timestamp": 1762128000
                      },
                      {
                        "close": 0.999749,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998511,
                        "timestamp": 1762214400
                      },
                      {
                        "close": 0.999653,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999064,
                        "timestamp": 1762300800
                      },
                      {
                        "close": 0.999621,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998328,
                        "timestamp": 1762387200
                      },
                      {
                        "close": 0.999863,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999015,
                        "timestamp": 1762473600
                      },
                      {
                        "close": 0.999961,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999452,
                        "timestamp": 1762560000
                      },
                      {
                        "close": 0.999754,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99924,
                        "timestamp": 1762646400
                      },
                      {
                        "close": 0.999391,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999242,
                        "timestamp": 1762732800
                      },
                      {
                        "close": 0.999726,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999159,
                        "timestamp": 1762819200
                      },
                      {
                        "close": 0.999418,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998937,
                        "timestamp": 1762905600
                      },
                      {
                        "close": 0.999937,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998893,
                        "timestamp": 1762992000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998596,
                        "timestamp": 1763078400
                      },
                      {
                        "close": 0.999921,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999132,
                        "timestamp": 1763164800
                      },
                      {
                        "close": 0.99985,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998893,
                        "timestamp": 1763251200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998753,
                        "timestamp": 1763337600
                      },
                      {
                        "close": 0.999973,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998451,
                        "timestamp": 1763424000
                      },
                      {
                        "close": 0.999529,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999168,
                        "timestamp": 1763510400
                      },
                      {
                        "close": 0.999601,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998835,
                        "timestamp": 1763596800
                      }
                    ],
                    "5d": [
                      {
                        "close": 0.999434,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998911,
                        "timestamp": 1763334000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999077,
                        "timestamp": 1763337600
                      },
                      {
                        "close": 0.999939,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999091,
                        "timestamp": 1763341200
                      },
                      {
                        "close": 0.999611,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998698,
                        "timestamp": 1763344800
                      },
                      {
                        "close": 0.999698,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999256,
                        "timestamp": 1763348400
                      },
                      {
                        "close": 0.999692,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998881,
                        "timestamp": 1763352000
                      },
                      {
                        "close": 0.999907,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99934,
                        "timestamp": 1763355600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999253,
                        "timestamp": 1763359200
                      },
                      {
                        "close": 0.999443,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999142,
                        "timestamp": 1763362800
                      },
                      {
                        "close": 0.999403,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999288,
                        "timestamp": 1763366400
                      },
                      {
                        "close": 0.999769,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999148,
                        "timestamp": 1763370000
                      },
                      {
                        "close": 0.999855,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998722,
                        "timestamp": 1763373600
                      },
                      {
                        "close": 0.999781,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999208,
                        "timestamp": 1763377200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999233,
                        "timestamp": 1763380800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999014,
                        "timestamp": 1763384400
                      },
                      {
                        "close": 0.999039,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999039,
                        "timestamp": 1763388000
                      },
                      {
                        "close": 0.999901,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99884,
                        "timestamp": 1763391600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999033,
                        "timestamp": 1763395200
                      },
                      {
                        "close": 0.999568,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999076,
                        "timestamp": 1763398800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99922,
                        "timestamp": 1763402400
                      },
                      {
                        "close": 0.99998,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998936,
                        "timestamp": 1763406000
                      },
                      {
                        "close": 0.999717,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998739,
                        "timestamp": 1763409600
                      },
                      {
                        "close": 0.999861,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999234,
                        "timestamp": 1763413200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999092,
                        "timestamp": 1763416800
                      },
                      {
                        "close": 0.999808,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999336,
                        "timestamp": 1763420400
                      },
                      {
                        "close": 0.999299,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998587,
                        "timestamp": 1763424000
                      },
                      {
                        "close": 0.999519,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998809,
                        "timestamp": 1763427600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998709,
                        "timestamp": 1763431200
                      },
                      {
                        "close": 0.999899,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998302,
                        "timestamp": 1763434800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998825,
                        "timestamp": 1763438400
                      },
                      {
                        "close": 0.999985,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999216,
                        "timestamp": 1763442000
                      },
                      {
                        "close": 0.999962,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999125,
                        "timestamp": 1763445600
                      },
                      {
                        "close": 0.999746,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999168,
                        "timestamp": 1763449200
                      },
                      {
                        "close": 0.999952,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998742,
                        "timestamp": 1763452800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999098,
                        "timestamp": 1763456400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999347,
                        "timestamp": 1763460000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999393,
                        "timestamp": 1763463600
                      },
                      {
                        "close": 0.999807,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998592,
                        "timestamp": 1763467200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99845,
                        "timestamp": 1763470800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998389,
                        "timestamp": 1763474400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998268,
                        "timestamp": 1763478000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999003,
                        "timestamp": 1763481600
                      },
                      {
                        "close": 0.999985,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999454,
                        "timestamp": 1763485200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999055,
                        "timestamp": 1763488800
                      },
                      {
                        "close": 0.999933,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99932,
                        "timestamp": 1763492400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999367,
                        "timestamp": 1763496000
                      },
                      {
                        "close": 0.999727,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999571,
                        "timestamp": 1763499600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998929,
                        "timestamp": 1763503200
                      },
                      {
                        "close": 0.999908,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999504,
                        "timestamp": 1763506800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999328,
                        "timestamp": 1763510400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999197,
                        "timestamp": 1763514000
                      },
                      {
                        "close": 0.999902,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999168,
                        "timestamp": 1763517600
                      },
                      {
                        "close": 0.999965,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999502,
                        "timestamp": 1763521200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999698,
                        "timestamp": 1763524800
                      },
                      {
                        "close": 0.999731,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999271,
                        "timestamp": 1763528400
                      },
                      {
                        "close": 0.999834,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999133,
                        "timestamp": 1763532000
                      },
                      {
                        "close": 0.999829,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999109,
                        "timestamp": 1763535600
                      },
                      {
                        "close": 0.999691,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999164,
                        "timestamp": 1763539200
                      },
                      {
                        "close": 0.999643,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999257,
                        "timestamp": 1763542800
                      },
                      {
                        "close": 0.999789,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999337,
                        "timestamp": 1763546400
                      },
                      {
                        "close": 0.999617,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999488,
                        "timestamp": 1763550000
                      },
                      {
                        "close": 0.9992,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999178,
                        "timestamp": 1763553600
                      },
                      {
                        "close": 0.999726,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999178,
                        "timestamp": 1763557200
                      },
                      {
                        "close": 0.999927,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998805,
                        "timestamp": 1763560800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99913,
                        "timestamp": 1763564400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999297,
                        "timestamp": 1763568000
                      },
                      {
                        "close": 0.999586,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999045,
                        "timestamp": 1763571600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999197,
                        "timestamp": 1763575200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999306,
                        "timestamp": 1763578800
                      },
                      {
                        "close": 0.999831,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999229,
                        "timestamp": 1763582400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99905,
                        "timestamp": 1763586000
                      },
                      {
                        "close": 0.999505,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999406,
                        "timestamp": 1763589600
                      },
                      {
                        "close": 0.999799,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999161,
                        "timestamp": 1763593200
                      },
                      {
                        "close": 0.999633,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999031,
                        "timestamp": 1763596800
                      },
                      {
                        "close": 0.99953,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99939,
                        "timestamp": 1763600400
                      },
                      {
                        "close": 0.999795,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999363,
                        "timestamp": 1763604000
                      },
                      {
                        "close": 0.999563,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999287,
                        "timestamp": 1763607600
                      },
                      {
                        "close": 0.999524,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999382,
                        "timestamp": 1763611200
                      },
                      {
                        "close": 0.999772,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999028,
                        "timestamp": 1763614800
                      },
                      {
                        "close": 0.999477,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999251,
                        "timestamp": 1763618400
                      },
                      {
                        "close": 0.999983,
                        "currency_code": "USD",
                        "high": 0.999985,
                        "low": 0.999177,
                        "timestamp": 1763622000
                      },
                      {
                        "close": 0.999533,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999224,
                        "timestamp": 1763625600
                      },
                      {
                        "close": 0.999933,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999215,
                        "timestamp": 1763629200
                      },
                      {
                        "close": 0.999774,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999518,
                        "timestamp": 1763632800
                      },
                      {
                        "close": 0.999895,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999059,
                        "timestamp": 1763636400
                      },
                      {
                        "close": 0.999994,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999421,
                        "timestamp": 1763640000
                      },
                      {
                        "close": 0.999986,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998806,
                        "timestamp": 1763643600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998967,
                        "timestamp": 1763647200
                      },
                      {
                        "close": 0.999763,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999287,
                        "timestamp": 1763650800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99885,
                        "timestamp": 1763654400
                      },
                      {
                        "close": 0.999794,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999083,
                        "timestamp": 1763658000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999011,
                        "timestamp": 1763661600
                      },
                      {
                        "close": 0.999681,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998868,
                        "timestamp": 1763665200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99905,
                        "timestamp": 1763668800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999243,
                        "timestamp": 1763672400
                      },
                      {
                        "close": 0.999611,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999166,
                        "timestamp": 1763676000
                      },
                      {
                        "close": 0.99998,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999285,
                        "timestamp": 1763679600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999103,
                        "timestamp": 1763683200
                      },
                      {
                        "close": 0.998832,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998795,
                        "timestamp": 1763686800
                      },
                      {
                        "close": 0.999998,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998303,
                        "timestamp": 1763690400
                      },
                      {
                        "close": 0.999195,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998634,
                        "timestamp": 1763694000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998812,
                        "timestamp": 1763697600
                      },
                      {
                        "close": 0.999286,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998593,
                        "timestamp": 1763701200
                      },
                      {
                        "close": 0.9995,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998518,
                        "timestamp": 1763704800
                      },
                      {
                        "close": 0.999341,
                        "currency_code": "USD",
                        "high": 0.999751,
                        "low": 0.999128,
                        "timestamp": 1763708400
                      }
                    ],
                    "5y": [
                      {
                        "close": 0.9892008090443228,
                        "currency_code": "USD",
                        "high": 0.9892008090443228,
                        "low": 0.9892008090443228,
                        "timestamp": 1689984000
                      },
                      {
                        "close": 1.0001815229648425,
                        "currency_code": "USD",
                        "high": 1.0156166895840075,
                        "low": 0.9970048682303255,
                        "timestamp": 1692576000
                      },
                      {
                        "close": 0.9993176780039713,
                        "currency_code": "USD",
                        "high": 1.0012104119418643,
                        "low": 0.9967743809559029,
                        "timestamp": 1695168000
                      },
                      {
                        "close": 0.9993503031888199,
                        "currency_code": "USD",
                        "high": 1.000409062040101,
                        "low": 0.9969273342697805,
                        "timestamp": 1697760000
                      },
                      {
                        "close": 1.0001549205585825,
                        "currency_code": "USD",
                        "high": 1.0002246154687153,
                        "low": 0.9969845110930868,
                        "timestamp": 1700352000
                      },
                      {
                        "close": 0.9998756954114192,
                        "currency_code": "USD",
                        "high": 1.0024105394870666,
                        "low": 0.9959828921367971,
                        "timestamp": 1702944000
                      },
                      {
                        "close": 0.9991697701570601,
                        "currency_code": "USD",
                        "high": 1.0034111393694147,
                        "low": 0.9971157869238798,
                        "timestamp": 1705536000
                      },
                      {
                        "close": 1.0003059258741773,
                        "currency_code": "USD",
                        "high": 1.0023386348574128,
                        "low": 0.9959611773259146,
                        "timestamp": 1708128000
                      },
                      {
                        "close": 0.999958,
                        "currency_code": "USD",
                        "high": 1.016,
                        "low": 0.989655,
                        "timestamp": 1710720000
                      },
                      {
                        "close": 0.998974,
                        "currency_code": "USD",
                        "high": 1.008,
                        "low": 0.9886,
                        "timestamp": 1713312000
                      },
                      {
                        "close": 0.998913,
                        "currency_code": "USD",
                        "high": 1.008,
                        "low": 0.992287,
                        "timestamp": 1715904000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.016,
                        "low": 0.97657,
                        "timestamp": 1718496000
                      },
                      {
                        "close": 0.999929,
                        "currency_code": "USD",
                        "high": 1.015,
                        "low": 0.984254,
                        "timestamp": 1721088000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.011,
                        "low": 0.981956,
                        "timestamp": 1723680000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.012,
                        "low": 0.99085,
                        "timestamp": 1726272000
                      },
                      {
                        "close": 1.002,
                        "currency_code": "USD",
                        "high": 1.01,
                        "low": 0.988024,
                        "timestamp": 1728864000
                      },
                      {
                        "close": 0.999483,
                        "currency_code": "USD",
                        "high": 1.01,
                        "low": 0.959426,
                        "timestamp": 1731456000
                      },
                      {
                        "close": 0.999537,
                        "currency_code": "USD",
                        "high": 1.009,
                        "low": 0.99184,
                        "timestamp": 1734048000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.016,
                        "low": 0.978146,
                        "timestamp": 1736640000
                      },
                      {
                        "close": 0.999868,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.993208,
                        "timestamp": 1739232000
                      },
                      {
                        "close": 0.999857,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997346,
                        "timestamp": 1741824000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998709,
                        "timestamp": 1744416000
                      },
                      {
                        "close": 0.999294,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998667,
                        "timestamp": 1747008000
                      },
                      {
                        "close": 0.999512,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998768,
                        "timestamp": 1749600000
                      },
                      {
                        "close": 0.999611,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998673,
                        "timestamp": 1752192000
                      },
                      {
                        "close": 0.999804,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998937,
                        "timestamp": 1754784000
                      },
                      {
                        "close": 0.999937,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.99726,
                        "timestamp": 1757376000
                      },
                      {
                        "close": 0.999863,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998328,
                        "timestamp": 1759968000
                      },
                      {
                        "close": 0.999601,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998451,
                        "timestamp": 1762560000
                      }
                    ],
                    "6m": [
                      {
                        "close": 0.999597,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998672,
                        "timestamp": 1747872000
                      },
                      {
                        "close": 0.999445,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998925,
                        "timestamp": 1747958400
                      },
                      {
                        "close": 0.999736,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998805,
                        "timestamp": 1748044800
                      },
                      {
                        "close": 0.999367,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99882,
                        "timestamp": 1748131200
                      },
                      {
                        "close": 0.999742,
                        "currency_code": "USD",
                        "high": 0.99986,
                        "low": 0.999043,
                        "timestamp": 1748217600
                      },
                      {
                        "close": 0.999515,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999007,
                        "timestamp": 1748304000
                      },
                      {
                        "close": 0.999731,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99919,
                        "timestamp": 1748390400
                      },
                      {
                        "close": 0.999341,
                        "currency_code": "USD",
                        "high": 0.999883,
                        "low": 0.999167,
                        "timestamp": 1748476800
                      },
                      {
                        "close": 0.999514,
                        "currency_code": "USD",
                        "high": 0.999885,
                        "low": 0.999255,
                        "timestamp": 1748563200
                      },
                      {
                        "close": 0.999325,
                        "currency_code": "USD",
                        "high": 0.999786,
                        "low": 0.999302,
                        "timestamp": 1748649600
                      },
                      {
                        "close": 0.999614,
                        "currency_code": "USD",
                        "high": 0.999793,
                        "low": 0.998824,
                        "timestamp": 1748736000
                      },
                      {
                        "close": 0.999626,
                        "currency_code": "USD",
                        "high": 0.999896,
                        "low": 0.998667,
                        "timestamp": 1748822400
                      },
                      {
                        "close": 0.999638,
                        "currency_code": "USD",
                        "high": 0.999807,
                        "low": 0.999306,
                        "timestamp": 1748908800
                      },
                      {
                        "close": 0.999636,
                        "currency_code": "USD",
                        "high": 0.999949,
                        "low": 0.999455,
                        "timestamp": 1748995200
                      },
                      {
                        "close": 0.999361,
                        "currency_code": "USD",
                        "high": 0.99998,
                        "low": 0.999205,
                        "timestamp": 1749081600
                      },
                      {
                        "close": 0.999188,
                        "currency_code": "USD",
                        "high": 0.999834,
                        "low": 0.998885,
                        "timestamp": 1749168000
                      },
                      {
                        "close": 0.999395,
                        "currency_code": "USD",
                        "high": 0.999756,
                        "low": 0.998669,
                        "timestamp": 1749254400
                      },
                      {
                        "close": 0.99988,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999235,
                        "timestamp": 1749340800
                      },
                      {
                        "close": 0.999446,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99922,
                        "timestamp": 1749427200
                      },
                      {
                        "close": 0.999294,
                        "currency_code": "USD",
                        "high": 0.999847,
                        "low": 0.999137,
                        "timestamp": 1749513600
                      },
                      {
                        "close": 0.999725,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999118,
                        "timestamp": 1749600000
                      },
                      {
                        "close": 0.999414,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99906,
                        "timestamp": 1749686400
                      },
                      {
                        "close": 0.999676,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998964,
                        "timestamp": 1749772800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999254,
                        "timestamp": 1749859200
                      },
                      {
                        "close": 0.999633,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999268,
                        "timestamp": 1749945600
                      },
                      {
                        "close": 0.998864,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998864,
                        "timestamp": 1750032000
                      },
                      {
                        "close": 0.999659,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999145,
                        "timestamp": 1750118400
                      },
                      {
                        "close": 0.999598,
                        "currency_code": "USD",
                        "high": 0.999979,
                        "low": 0.999267,
                        "timestamp": 1750204800
                      },
                      {
                        "close": 0.999444,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.9992,
                        "timestamp": 1750291200
                      },
                      {
                        "close": 0.999473,
                        "currency_code": "USD",
                        "high": 0.999953,
                        "low": 0.999109,
                        "timestamp": 1750377600
                      },
                      {
                        "close": 0.999644,
                        "currency_code": "USD",
                        "high": 0.999927,
                        "low": 0.999224,
                        "timestamp": 1750464000
                      },
                      {
                        "close": 0.999942,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999287,
                        "timestamp": 1750550400
                      },
                      {
                        "close": 0.999871,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998768,
                        "timestamp": 1750636800
                      },
                      {
                        "close": 0.99975,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99917,
                        "timestamp": 1750723200
                      },
                      {
                        "close": 0.999541,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998865,
                        "timestamp": 1750809600
                      },
                      {
                        "close": 0.999431,
                        "currency_code": "USD",
                        "high": 0.99991,
                        "low": 0.999345,
                        "timestamp": 1750896000
                      },
                      {
                        "close": 0.999504,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999182,
                        "timestamp": 1750982400
                      },
                      {
                        "close": 0.999757,
                        "currency_code": "USD",
                        "high": 0.999856,
                        "low": 0.999364,
                        "timestamp": 1751068800
                      },
                      {
                        "close": 0.999608,
                        "currency_code": "USD",
                        "high": 0.999865,
                        "low": 0.999283,
                        "timestamp": 1751155200
                      },
                      {
                        "close": 0.999878,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999173,
                        "timestamp": 1751241600
                      },
                      {
                        "close": 0.999541,
                        "currency_code": "USD",
                        "high": 0.999914,
                        "low": 0.999082,
                        "timestamp": 1751328000
                      },
                      {
                        "close": 0.999513,
                        "currency_code": "USD",
                        "high": 0.999971,
                        "low": 0.999373,
                        "timestamp": 1751414400
                      },
                      {
                        "close": 0.99979,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998993,
                        "timestamp": 1751500800
                      },
                      {
                        "close": 0.999849,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999399,
                        "timestamp": 1751587200
                      },
                      {
                        "close": 0.999735,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999354,
                        "timestamp": 1751673600
                      },
                      {
                        "close": 0.999606,
                        "currency_code": "USD",
                        "high": 0.999904,
                        "low": 0.999077,
                        "timestamp": 1751760000
                      },
                      {
                        "close": 0.999887,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998904,
                        "timestamp": 1751846400
                      },
                      {
                        "close": 0.9998,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999447,
                        "timestamp": 1751932800
                      },
                      {
                        "close": 0.999636,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998979,
                        "timestamp": 1752019200
                      },
                      {
                        "close": 0.999512,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999187,
                        "timestamp": 1752105600
                      },
                      {
                        "close": 0.999537,
                        "currency_code": "USD",
                        "high": 0.999945,
                        "low": 0.99905,
                        "timestamp": 1752192000
                      },
                      {
                        "close": 0.999581,
                        "currency_code": "USD",
                        "high": 0.999886,
                        "low": 0.999098,
                        "timestamp": 1752278400
                      },
                      {
                        "close": 0.999651,
                        "currency_code": "USD",
                        "high": 0.999773,
                        "low": 0.999141,
                        "timestamp": 1752364800
                      },
                      {
                        "close": 0.999694,
                        "currency_code": "USD",
                        "high": 0.999785,
                        "low": 0.998938,
                        "timestamp": 1752451200
                      },
                      {
                        "close": 0.999647,
                        "currency_code": "USD",
                        "high": 0.99996,
                        "low": 0.998674,
                        "timestamp": 1752537600
                      },
                      {
                        "close": 0.999773,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999115,
                        "timestamp": 1752624000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999152,
                        "timestamp": 1752710400
                      },
                      {
                        "close": 0.999678,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999431,
                        "timestamp": 1752796800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999597,
                        "timestamp": 1752883200
                      },
                      {
                        "close": 0.999532,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999223,
                        "timestamp": 1752969600
                      },
                      {
                        "close": 0.99965,
                        "currency_code": "USD",
                        "high": 0.99994,
                        "low": 0.99927,
                        "timestamp": 1753056000
                      },
                      {
                        "close": 0.999762,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.9995,
                        "timestamp": 1753142400
                      },
                      {
                        "close": 0.999745,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999279,
                        "timestamp": 1753228800
                      },
                      {
                        "close": 0.999351,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999302,
                        "timestamp": 1753315200
                      },
                      {
                        "close": 0.999906,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998862,
                        "timestamp": 1753401600
                      },
                      {
                        "close": 0.999759,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999341,
                        "timestamp": 1753488000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999234,
                        "timestamp": 1753574400
                      },
                      {
                        "close": 0.999935,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999058,
                        "timestamp": 1753660800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999073,
                        "timestamp": 1753747200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999035,
                        "timestamp": 1753833600
                      },
                      {
                        "close": 0.999331,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999041,
                        "timestamp": 1753920000
                      },
                      {
                        "close": 0.999742,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998673,
                        "timestamp": 1754006400
                      },
                      {
                        "close": 0.999513,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998953,
                        "timestamp": 1754092800
                      },
                      {
                        "close": 0.999652,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999081,
                        "timestamp": 1754179200
                      },
                      {
                        "close": 0.999372,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998819,
                        "timestamp": 1754265600
                      },
                      {
                        "close": 0.999867,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998779,
                        "timestamp": 1754352000
                      },
                      {
                        "close": 0.999742,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999058,
                        "timestamp": 1754438400
                      },
                      {
                        "close": 0.999908,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998825,
                        "timestamp": 1754524800
                      },
                      {
                        "close": 0.999777,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999011,
                        "timestamp": 1754611200
                      },
                      {
                        "close": 0.999611,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999235,
                        "timestamp": 1754697600
                      },
                      {
                        "close": 0.999598,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99895,
                        "timestamp": 1754784000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998937,
                        "timestamp": 1754870400
                      },
                      {
                        "close": 0.999705,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999029,
                        "timestamp": 1754956800
                      },
                      {
                        "close": 0.999506,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999129,
                        "timestamp": 1755043200
                      },
                      {
                        "close": 0.999782,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99919,
                        "timestamp": 1755129600
                      },
                      {
                        "close": 0.99976,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999279,
                        "timestamp": 1755216000
                      },
                      {
                        "close": 0.999932,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999546,
                        "timestamp": 1755302400
                      },
                      {
                        "close": 0.999958,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999562,
                        "timestamp": 1755388800
                      },
                      {
                        "close": 0.999863,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999513,
                        "timestamp": 1755475200
                      },
                      {
                        "close": 0.999872,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999591,
                        "timestamp": 1755561600
                      },
                      {
                        "close": 0.999845,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999379,
                        "timestamp": 1755648000
                      },
                      {
                        "close": 0.999484,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999302,
                        "timestamp": 1755734400
                      },
                      {
                        "close": 0.99963,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999121,
                        "timestamp": 1755820800
                      },
                      {
                        "close": 0.999578,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999216,
                        "timestamp": 1755907200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999247,
                        "timestamp": 1755993600
                      },
                      {
                        "close": 0.999783,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998956,
                        "timestamp": 1756080000
                      },
                      {
                        "close": 0.999906,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999215,
                        "timestamp": 1756166400
                      },
                      {
                        "close": 0.999837,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999131,
                        "timestamp": 1756252800
                      },
                      {
                        "close": 0.999465,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999072,
                        "timestamp": 1756339200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998987,
                        "timestamp": 1756425600
                      },
                      {
                        "close": 0.999448,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999349,
                        "timestamp": 1756512000
                      },
                      {
                        "close": 0.999408,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999248,
                        "timestamp": 1756598400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999212,
                        "timestamp": 1756684800
                      },
                      {
                        "close": 0.999702,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999196,
                        "timestamp": 1756771200
                      },
                      {
                        "close": 0.999858,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999277,
                        "timestamp": 1756857600
                      },
                      {
                        "close": 0.999709,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999229,
                        "timestamp": 1756944000
                      },
                      {
                        "close": 0.999724,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999132,
                        "timestamp": 1757030400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998964,
                        "timestamp": 1757116800
                      },
                      {
                        "close": 0.999965,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999444,
                        "timestamp": 1757203200
                      },
                      {
                        "close": 0.999804,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99921,
                        "timestamp": 1757289600
                      },
                      {
                        "close": 0.99985,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999349,
                        "timestamp": 1757376000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999157,
                        "timestamp": 1757462400
                      },
                      {
                        "close": 0.999871,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999017,
                        "timestamp": 1757548800
                      },
                      {
                        "close": 0.999924,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999302,
                        "timestamp": 1757635200
                      },
                      {
                        "close": 0.999793,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999428,
                        "timestamp": 1757721600
                      },
                      {
                        "close": 0.999763,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999603,
                        "timestamp": 1757808000
                      },
                      {
                        "close": 0.999843,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999357,
                        "timestamp": 1757894400
                      },
                      {
                        "close": 0.999837,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999452,
                        "timestamp": 1757980800
                      },
                      {
                        "close": 0.999759,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999174,
                        "timestamp": 1758067200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998666,
                        "timestamp": 1758153600
                      },
                      {
                        "close": 0.999878,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998049,
                        "timestamp": 1758240000
                      },
                      {
                        "close": 0.999783,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998635,
                        "timestamp": 1758326400
                      },
                      {
                        "close": 0.999783,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999345,
                        "timestamp": 1758412800
                      },
                      {
                        "close": 0.999736,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999073,
                        "timestamp": 1758499200
                      },
                      {
                        "close": 0.99988,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998516,
                        "timestamp": 1758585600
                      },
                      {
                        "close": 0.999861,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998455,
                        "timestamp": 1758672000
                      },
                      {
                        "close": 0.999899,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997671,
                        "timestamp": 1758758400
                      },
                      {
                        "close": 0.999737,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.997598,
                        "timestamp": 1758844800
                      },
                      {
                        "close": 0.99967,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.999386,
                        "timestamp": 1758931200
                      },
                      {
                        "close": 0.999996,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.999423,
                        "timestamp": 1759017600
                      },
                      {
                        "close": 0.999812,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.997591,
                        "timestamp": 1759104000
                      },
                      {
                        "close": 0.999759,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.997367,
                        "timestamp": 1759190400
                      },
                      {
                        "close": 0.999929,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99726,
                        "timestamp": 1759276800
                      },
                      {
                        "close": 0.999761,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999165,
                        "timestamp": 1759363200
                      },
                      {
                        "close": 0.999703,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999306,
                        "timestamp": 1759449600
                      },
                      {
                        "close": 0.999861,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999106,
                        "timestamp": 1759536000
                      },
                      {
                        "close": 0.999947,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998487,
                        "timestamp": 1759622400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999115,
                        "timestamp": 1759708800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999038,
                        "timestamp": 1759795200
                      },
                      {
                        "close": 0.999937,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998948,
                        "timestamp": 1759881600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999399,
                        "timestamp": 1759968000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998834,
                        "timestamp": 1760054400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998707,
                        "timestamp": 1760140800
                      },
                      {
                        "close": 0.999948,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999256,
                        "timestamp": 1760227200
                      },
                      {
                        "close": 0.999932,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999409,
                        "timestamp": 1760313600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999421,
                        "timestamp": 1760400000
                      },
                      {
                        "close": 0.999903,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999268,
                        "timestamp": 1760486400
                      },
                      {
                        "close": 0.999696,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999296,
                        "timestamp": 1760572800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999042,
                        "timestamp": 1760659200
                      },
                      {
                        "close": 0.999969,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.9993,
                        "timestamp": 1760745600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999427,
                        "timestamp": 1760832000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999327,
                        "timestamp": 1760918400
                      },
                      {
                        "close": 0.999815,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999049,
                        "timestamp": 1761004800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99923,
                        "timestamp": 1761091200
                      },
                      {
                        "close": 0.9999,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999364,
                        "timestamp": 1761177600
                      },
                      {
                        "close": 0.999947,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999127,
                        "timestamp": 1761264000
                      },
                      {
                        "close": 0.999872,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999299,
                        "timestamp": 1761350400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999524,
                        "timestamp": 1761436800
                      },
                      {
                        "close": 0.999962,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999389,
                        "timestamp": 1761523200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999103,
                        "timestamp": 1761609600
                      },
                      {
                        "close": 0.999957,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99874,
                        "timestamp": 1761696000
                      },
                      {
                        "close": 0.999724,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999012,
                        "timestamp": 1761782400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998979,
                        "timestamp": 1761868800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999334,
                        "timestamp": 1761955200
                      },
                      {
                        "close": 0.999953,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99945,
                        "timestamp": 1762041600
                      },
                      {
                        "close": 0.999845,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998958,
                        "timestamp": 1762128000
                      },
                      {
                        "close": 0.999749,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998511,
                        "timestamp": 1762214400
                      },
                      {
                        "close": 0.999653,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999064,
                        "timestamp": 1762300800
                      },
                      {
                        "close": 0.999621,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998328,
                        "timestamp": 1762387200
                      },
                      {
                        "close": 0.999863,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999015,
                        "timestamp": 1762473600
                      },
                      {
                        "close": 0.999961,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999452,
                        "timestamp": 1762560000
                      },
                      {
                        "close": 0.999754,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99924,
                        "timestamp": 1762646400
                      },
                      {
                        "close": 0.999391,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999242,
                        "timestamp": 1762732800
                      },
                      {
                        "close": 0.999726,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999159,
                        "timestamp": 1762819200
                      },
                      {
                        "close": 0.999418,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998937,
                        "timestamp": 1762905600
                      },
                      {
                        "close": 0.999937,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998893,
                        "timestamp": 1762992000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998596,
                        "timestamp": 1763078400
                      },
                      {
                        "close": 0.999921,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999132,
                        "timestamp": 1763164800
                      },
                      {
                        "close": 0.99985,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998893,
                        "timestamp": 1763251200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998753,
                        "timestamp": 1763337600
                      },
                      {
                        "close": 0.999973,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998451,
                        "timestamp": 1763424000
                      },
                      {
                        "close": 0.999529,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999168,
                        "timestamp": 1763510400
                      },
                      {
                        "close": 0.999601,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998835,
                        "timestamp": 1763596800
                      }
                    ],
                    "max": [
                      {
                        "close": 0.9892008090443228,
                        "currency_code": "USD",
                        "high": 0.9892008090443228,
                        "low": 0.9892008090443228,
                        "timestamp": 1689984000
                      },
                      {
                        "close": 1.0001815229648425,
                        "currency_code": "USD",
                        "high": 1.0156166895840075,
                        "low": 0.9970048682303255,
                        "timestamp": 1692576000
                      },
                      {
                        "close": 0.9993176780039713,
                        "currency_code": "USD",
                        "high": 1.0012104119418643,
                        "low": 0.9967743809559029,
                        "timestamp": 1695168000
                      },
                      {
                        "close": 0.9993503031888199,
                        "currency_code": "USD",
                        "high": 1.000409062040101,
                        "low": 0.9969273342697805,
                        "timestamp": 1697760000
                      },
                      {
                        "close": 1.0001549205585825,
                        "currency_code": "USD",
                        "high": 1.0002246154687153,
                        "low": 0.9969845110930868,
                        "timestamp": 1700352000
                      },
                      {
                        "close": 0.9998756954114192,
                        "currency_code": "USD",
                        "high": 1.0024105394870666,
                        "low": 0.9959828921367971,
                        "timestamp": 1702944000
                      },
                      {
                        "close": 0.9991697701570601,
                        "currency_code": "USD",
                        "high": 1.0034111393694147,
                        "low": 0.9971157869238798,
                        "timestamp": 1705536000
                      },
                      {
                        "close": 1.0003059258741773,
                        "currency_code": "USD",
                        "high": 1.0023386348574128,
                        "low": 0.9959611773259146,
                        "timestamp": 1708128000
                      },
                      {
                        "close": 0.999958,
                        "currency_code": "USD",
                        "high": 1.016,
                        "low": 0.989655,
                        "timestamp": 1710720000
                      },
                      {
                        "close": 0.998974,
                        "currency_code": "USD",
                        "high": 1.008,
                        "low": 0.9886,
                        "timestamp": 1713312000
                      },
                      {
                        "close": 0.998913,
                        "currency_code": "USD",
                        "high": 1.008,
                        "low": 0.992287,
                        "timestamp": 1715904000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.016,
                        "low": 0.97657,
                        "timestamp": 1718496000
                      },
                      {
                        "close": 0.999929,
                        "currency_code": "USD",
                        "high": 1.015,
                        "low": 0.984254,
                        "timestamp": 1721088000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.011,
                        "low": 0.981956,
                        "timestamp": 1723680000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.012,
                        "low": 0.99085,
                        "timestamp": 1726272000
                      },
                      {
                        "close": 1.002,
                        "currency_code": "USD",
                        "high": 1.01,
                        "low": 0.988024,
                        "timestamp": 1728864000
                      },
                      {
                        "close": 0.999483,
                        "currency_code": "USD",
                        "high": 1.01,
                        "low": 0.959426,
                        "timestamp": 1731456000
                      },
                      {
                        "close": 0.999537,
                        "currency_code": "USD",
                        "high": 1.009,
                        "low": 0.99184,
                        "timestamp": 1734048000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.016,
                        "low": 0.978146,
                        "timestamp": 1736640000
                      },
                      {
                        "close": 0.999868,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.993208,
                        "timestamp": 1739232000
                      },
                      {
                        "close": 0.999857,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997346,
                        "timestamp": 1741824000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998709,
                        "timestamp": 1744416000
                      },
                      {
                        "close": 0.999294,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998667,
                        "timestamp": 1747008000
                      },
                      {
                        "close": 0.999512,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998768,
                        "timestamp": 1749600000
                      },
                      {
                        "close": 0.999611,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998673,
                        "timestamp": 1752192000
                      },
                      {
                        "close": 0.999804,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998937,
                        "timestamp": 1754784000
                      },
                      {
                        "close": 0.999937,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.99726,
                        "timestamp": 1757376000
                      },
                      {
                        "close": 0.999863,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998328,
                        "timestamp": 1759968000
                      },
                      {
                        "close": 0.999601,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998451,
                        "timestamp": 1762560000
                      }
                    ],
                    "ytd": [
                      {
                        "close": 0.999294,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.997396,
                        "timestamp": 1735689600
                      },
                      {
                        "close": 0.999743,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.996306,
                        "timestamp": 1735776000
                      },
                      {
                        "close": 0.999683,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.997661,
                        "timestamp": 1735862400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997077,
                        "timestamp": 1735948800
                      },
                      {
                        "close": 0.999837,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.998013,
                        "timestamp": 1736035200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.995804,
                        "timestamp": 1736121600
                      },
                      {
                        "close": 0.999857,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.993702,
                        "timestamp": 1736208000
                      },
                      {
                        "close": 0.999486,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.995348,
                        "timestamp": 1736294400
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.99184,
                        "timestamp": 1736380800
                      },
                      {
                        "close": 0.99986,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.992508,
                        "timestamp": 1736467200
                      },
                      {
                        "close": 0.999537,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.99794,
                        "timestamp": 1736553600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997628,
                        "timestamp": 1736640000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.014,
                        "low": 0.992923,
                        "timestamp": 1736726400
                      },
                      {
                        "close": 0.999961,
                        "currency_code": "USD",
                        "high": 1.008,
                        "low": 0.99494,
                        "timestamp": 1736812800
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.996924,
                        "timestamp": 1736899200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.993447,
                        "timestamp": 1736985600
                      },
                      {
                        "close": 0.999777,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.995588,
                        "timestamp": 1737072000
                      },
                      {
                        "close": 0.999674,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.994448,
                        "timestamp": 1737158400
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.008,
                        "low": 0.98469,
                        "timestamp": 1737244800
                      },
                      {
                        "close": 0.998593,
                        "currency_code": "USD",
                        "high": 1.016,
                        "low": 0.978146,
                        "timestamp": 1737331200
                      },
                      {
                        "close": 1.002,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.993054,
                        "timestamp": 1737417600
                      },
                      {
                        "close": 0.999368,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.99725,
                        "timestamp": 1737504000
                      },
                      {
                        "close": 0.999089,
                        "currency_code": "USD",
                        "high": 1.011,
                        "low": 0.987658,
                        "timestamp": 1737590400
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.997098,
                        "timestamp": 1737676800
                      },
                      {
                        "close": 0.999744,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998861,
                        "timestamp": 1737763200
                      },
                      {
                        "close": 0.998347,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.997491,
                        "timestamp": 1737849600
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.994705,
                        "timestamp": 1737936000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.996743,
                        "timestamp": 1738022400
                      },
                      {
                        "close": 0.999447,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.995221,
                        "timestamp": 1738108800
                      },
                      {
                        "close": 0.998796,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.996861,
                        "timestamp": 1738195200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.99633,
                        "timestamp": 1738281600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.996966,
                        "timestamp": 1738368000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.994198,
                        "timestamp": 1738454400
                      },
                      {
                        "close": 0.999403,
                        "currency_code": "USD",
                        "high": 1.008,
                        "low": 0.987048,
                        "timestamp": 1738540800
                      },
                      {
                        "close": 1.002,
                        "currency_code": "USD",
                        "high": 1.006,
                        "low": 0.98999,
                        "timestamp": 1738627200
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.992324,
                        "timestamp": 1738713600
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.993846,
                        "timestamp": 1738800000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.993298,
                        "timestamp": 1738886400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998256,
                        "timestamp": 1738972800
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.996879,
                        "timestamp": 1739059200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.995701,
                        "timestamp": 1739145600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997373,
                        "timestamp": 1739232000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.993554,
                        "timestamp": 1739318400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.997647,
                        "timestamp": 1739404800
                      },
                      {
                        "close": 0.999957,
                        "currency_code": "USD",
                        "high": 1.007,
                        "low": 0.996389,
                        "timestamp": 1739491200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998206,
                        "timestamp": 1739577600
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998816,
                        "timestamp": 1739664000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.996878,
                        "timestamp": 1739750400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.997258,
                        "timestamp": 1739836800
                      },
                      {
                        "close": 0.999451,
                        "currency_code": "USD",
                        "high": 1.004,
                        "low": 0.996994,
                        "timestamp": 1739923200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.995987,
                        "timestamp": 1740009600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.99652,
                        "timestamp": 1740096000
                      },
                      {
                        "close": 0.999941,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.999136,
                        "timestamp": 1740182400
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998357,
                        "timestamp": 1740268800
                      },
                      {
                        "close": 0.999271,
                        "currency_code": "USD",
                        "high": 1.003,
                        "low": 0.996668,
                        "timestamp": 1740355200
                      },
                      {
                        "close": 0.999425,
                        "currency_code": "USD",
                        "high": 1.005,
                        "low": 0.993208,
                        "timestamp": 1740441600
                      },
                      {
                        "close": 0.999638,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99932,
                        "timestamp": 1740528000
                      },
                      {
                        "close": 0.999758,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998519,
                        "timestamp": 1740614400
                      },
                      {
                        "close": 0.999982,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998408,
                        "timestamp": 1740700800
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999147,
                        "timestamp": 1740787200
                      },
                      {
                        "close": 0.99893,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998625,
                        "timestamp": 1740873600
                      },
                      {
                        "close": 0.998805,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998172,
                        "timestamp": 1740960000
                      },
                      {
                        "close": 0.999498,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.997447,
                        "timestamp": 1741046400
                      },
                      {
                        "close": 0.999918,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998607,
                        "timestamp": 1741132800
                      },
                      {
                        "close": 0.998361,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998272,
                        "timestamp": 1741219200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997452,
                        "timestamp": 1741305600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998617,
                        "timestamp": 1741392000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998024,
                        "timestamp": 1741478400
                      },
                      {
                        "close": 0.99985,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997659,
                        "timestamp": 1741564800
                      },
                      {
                        "close": 0.999066,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998414,
                        "timestamp": 1741651200
                      },
                      {
                        "close": 0.999868,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998417,
                        "timestamp": 1741737600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997953,
                        "timestamp": 1741824000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998097,
                        "timestamp": 1741910400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998964,
                        "timestamp": 1741996800
                      },
                      {
                        "close": 0.999781,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998429,
                        "timestamp": 1742083200
                      },
                      {
                        "close": 0.999828,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998066,
                        "timestamp": 1742169600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.997346,
                        "timestamp": 1742256000
                      },
                      {
                        "close": 0.999498,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99863,
                        "timestamp": 1742342400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998733,
                        "timestamp": 1742428800
                      },
                      {
                        "close": 0.99973,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998958,
                        "timestamp": 1742515200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999396,
                        "timestamp": 1742601600
                      },
                      {
                        "close": 0.999562,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999287,
                        "timestamp": 1742688000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999165,
                        "timestamp": 1742774400
                      },
                      {
                        "close": 0.999688,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999107,
                        "timestamp": 1742860800
                      },
                      {
                        "close": 0.99992,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999136,
                        "timestamp": 1742947200
                      },
                      {
                        "close": 0.999581,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998507,
                        "timestamp": 1743033600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99854,
                        "timestamp": 1743120000
                      },
                      {
                        "close": 0.999981,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999175,
                        "timestamp": 1743206400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998713,
                        "timestamp": 1743292800
                      },
                      {
                        "close": 0.999669,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998649,
                        "timestamp": 1743379200
                      },
                      {
                        "close": 0.999453,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998751,
                        "timestamp": 1743465600
                      },
                      {
                        "close": 0.999858,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998626,
                        "timestamp": 1743552000
                      },
                      {
                        "close": 0.99956,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99863,
                        "timestamp": 1743638400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998658,
                        "timestamp": 1743724800
                      },
                      {
                        "close": 0.999794,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999122,
                        "timestamp": 1743811200
                      },
                      {
                        "close": 0.998962,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998276,
                        "timestamp": 1743897600
                      },
                      {
                        "close": 0.999908,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99872,
                        "timestamp": 1743984000
                      },
                      {
                        "close": 0.999812,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998408,
                        "timestamp": 1744070400
                      },
                      {
                        "close": 0.999382,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998534,
                        "timestamp": 1744156800
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998519,
                        "timestamp": 1744243200
                      },
                      {
                        "close": 0.999857,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998543,
                        "timestamp": 1744329600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998709,
                        "timestamp": 1744416000
                      },
                      {
                        "close": 1.001,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998796,
                        "timestamp": 1744502400
                      },
                      {
                        "close": 0.999203,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998793,
                        "timestamp": 1744588800
                      },
                      {
                        "close": 0.999758,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999063,
                        "timestamp": 1744675200
                      },
                      {
                        "close": 0.999615,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999092,
                        "timestamp": 1744761600
                      },
                      {
                        "close": 0.999792,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998969,
                        "timestamp": 1744848000
                      },
                      {
                        "close": 0.999807,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999231,
                        "timestamp": 1744934400
                      },
                      {
                        "close": 0.999871,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999494,
                        "timestamp": 1745020800
                      },
                      {
                        "close": 0.999891,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999367,
                        "timestamp": 1745107200
                      },
                      {
                        "close": 0.999842,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999184,
                        "timestamp": 1745193600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999171,
                        "timestamp": 1745280000
                      },
                      {
                        "close": 0.99995,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999293,
                        "timestamp": 1745366400
                      },
                      {
                        "close": 0.999989,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999372,
                        "timestamp": 1745452800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999388,
                        "timestamp": 1745539200
                      },
                      {
                        "close": 0.999854,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999353,
                        "timestamp": 1745625600
                      },
                      {
                        "close": 0.99986,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999549,
                        "timestamp": 1745712000
                      },
                      {
                        "close": 0.999927,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999302,
                        "timestamp": 1745798400
                      },
                      {
                        "close": 0.999941,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999261,
                        "timestamp": 1745884800
                      },
                      {
                        "close": 0.999511,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99912,
                        "timestamp": 1745971200
                      },
                      {
                        "close": 0.999704,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999319,
                        "timestamp": 1746057600
                      },
                      {
                        "close": 0.999536,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999439,
                        "timestamp": 1746144000
                      },
                      {
                        "close": 0.999829,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999262,
                        "timestamp": 1746230400
                      },
                      {
                        "close": 0.99977,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999136,
                        "timestamp": 1746316800
                      },
                      {
                        "close": 0.999562,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999379,
                        "timestamp": 1746403200
                      },
                      {
                        "close": 0.999607,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999376,
                        "timestamp": 1746489600
                      },
                      {
                        "close": 0.999649,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999382,
                        "timestamp": 1746576000
                      },
                      {
                        "close": 0.999776,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999291,
                        "timestamp": 1746662400
                      },
                      {
                        "close": 0.999738,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999045,
                        "timestamp": 1746748800
                      },
                      {
                        "close": 0.999947,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999397,
                        "timestamp": 1746835200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999455,
                        "timestamp": 1746921600
                      },
                      {
                        "close": 0.999871,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999341,
                        "timestamp": 1747008000
                      },
                      {
                        "close": 0.99989,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999319,
                        "timestamp": 1747094400
                      },
                      {
                        "close": 0.999786,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999508,
                        "timestamp": 1747180800
                      },
                      {
                        "close": 0.999674,
                        "currency_code": "USD",
                        "high": 0.999992,
                        "low": 0.999323,
                        "timestamp": 1747267200
                      },
                      {
                        "close": 0.999699,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999241,
                        "timestamp": 1747353600
                      },
                      {
                        "close": 0.999633,
                        "currency_code": "USD",
                        "high": 0.999833,
                        "low": 0.999351,
                        "timestamp": 1747440000
                      },
                      {
                        "close": 0.999636,
                        "currency_code": "USD",
                        "high": 0.999792,
                        "low": 0.999481,
                        "timestamp": 1747526400
                      },
                      {
                        "close": 0.999709,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999227,
                        "timestamp": 1747612800
                      },
                      {
                        "close": 0.999584,
                        "currency_code": "USD",
                        "high": 0.999895,
                        "low": 0.99924,
                        "timestamp": 1747699200
                      },
                      {
                        "close": 0.99965,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999193,
                        "timestamp": 1747785600
                      },
                      {
                        "close": 0.999597,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998672,
                        "timestamp": 1747872000
                      },
                      {
                        "close": 0.999445,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998925,
                        "timestamp": 1747958400
                      },
                      {
                        "close": 0.999736,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998805,
                        "timestamp": 1748044800
                      },
                      {
                        "close": 0.999367,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99882,
                        "timestamp": 1748131200
                      },
                      {
                        "close": 0.999742,
                        "currency_code": "USD",
                        "high": 0.99986,
                        "low": 0.999043,
                        "timestamp": 1748217600
                      },
                      {
                        "close": 0.999515,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999007,
                        "timestamp": 1748304000
                      },
                      {
                        "close": 0.999731,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99919,
                        "timestamp": 1748390400
                      },
                      {
                        "close": 0.999341,
                        "currency_code": "USD",
                        "high": 0.999883,
                        "low": 0.999167,
                        "timestamp": 1748476800
                      },
                      {
                        "close": 0.999514,
                        "currency_code": "USD",
                        "high": 0.999885,
                        "low": 0.999255,
                        "timestamp": 1748563200
                      },
                      {
                        "close": 0.999325,
                        "currency_code": "USD",
                        "high": 0.999786,
                        "low": 0.999302,
                        "timestamp": 1748649600
                      },
                      {
                        "close": 0.999614,
                        "currency_code": "USD",
                        "high": 0.999793,
                        "low": 0.998824,
                        "timestamp": 1748736000
                      },
                      {
                        "close": 0.999626,
                        "currency_code": "USD",
                        "high": 0.999896,
                        "low": 0.998667,
                        "timestamp": 1748822400
                      },
                      {
                        "close": 0.999638,
                        "currency_code": "USD",
                        "high": 0.999807,
                        "low": 0.999306,
                        "timestamp": 1748908800
                      },
                      {
                        "close": 0.999636,
                        "currency_code": "USD",
                        "high": 0.999949,
                        "low": 0.999455,
                        "timestamp": 1748995200
                      },
                      {
                        "close": 0.999361,
                        "currency_code": "USD",
                        "high": 0.99998,
                        "low": 0.999205,
                        "timestamp": 1749081600
                      },
                      {
                        "close": 0.999188,
                        "currency_code": "USD",
                        "high": 0.999834,
                        "low": 0.998885,
                        "timestamp": 1749168000
                      },
                      {
                        "close": 0.999395,
                        "currency_code": "USD",
                        "high": 0.999756,
                        "low": 0.998669,
                        "timestamp": 1749254400
                      },
                      {
                        "close": 0.99988,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999235,
                        "timestamp": 1749340800
                      },
                      {
                        "close": 0.999446,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99922,
                        "timestamp": 1749427200
                      },
                      {
                        "close": 0.999294,
                        "currency_code": "USD",
                        "high": 0.999847,
                        "low": 0.999137,
                        "timestamp": 1749513600
                      },
                      {
                        "close": 0.999725,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999118,
                        "timestamp": 1749600000
                      },
                      {
                        "close": 0.999414,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99906,
                        "timestamp": 1749686400
                      },
                      {
                        "close": 0.999676,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998964,
                        "timestamp": 1749772800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999254,
                        "timestamp": 1749859200
                      },
                      {
                        "close": 0.999633,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999268,
                        "timestamp": 1749945600
                      },
                      {
                        "close": 0.998864,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998864,
                        "timestamp": 1750032000
                      },
                      {
                        "close": 0.999659,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999145,
                        "timestamp": 1750118400
                      },
                      {
                        "close": 0.999598,
                        "currency_code": "USD",
                        "high": 0.999979,
                        "low": 0.999267,
                        "timestamp": 1750204800
                      },
                      {
                        "close": 0.999444,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.9992,
                        "timestamp": 1750291200
                      },
                      {
                        "close": 0.999473,
                        "currency_code": "USD",
                        "high": 0.999953,
                        "low": 0.999109,
                        "timestamp": 1750377600
                      },
                      {
                        "close": 0.999644,
                        "currency_code": "USD",
                        "high": 0.999927,
                        "low": 0.999224,
                        "timestamp": 1750464000
                      },
                      {
                        "close": 0.999942,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999287,
                        "timestamp": 1750550400
                      },
                      {
                        "close": 0.999871,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998768,
                        "timestamp": 1750636800
                      },
                      {
                        "close": 0.99975,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99917,
                        "timestamp": 1750723200
                      },
                      {
                        "close": 0.999541,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998865,
                        "timestamp": 1750809600
                      },
                      {
                        "close": 0.999431,
                        "currency_code": "USD",
                        "high": 0.99991,
                        "low": 0.999345,
                        "timestamp": 1750896000
                      },
                      {
                        "close": 0.999504,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999182,
                        "timestamp": 1750982400
                      },
                      {
                        "close": 0.999757,
                        "currency_code": "USD",
                        "high": 0.999856,
                        "low": 0.999364,
                        "timestamp": 1751068800
                      },
                      {
                        "close": 0.999608,
                        "currency_code": "USD",
                        "high": 0.999865,
                        "low": 0.999283,
                        "timestamp": 1751155200
                      },
                      {
                        "close": 0.999878,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999173,
                        "timestamp": 1751241600
                      },
                      {
                        "close": 0.999541,
                        "currency_code": "USD",
                        "high": 0.999914,
                        "low": 0.999082,
                        "timestamp": 1751328000
                      },
                      {
                        "close": 0.999513,
                        "currency_code": "USD",
                        "high": 0.999971,
                        "low": 0.999373,
                        "timestamp": 1751414400
                      },
                      {
                        "close": 0.99979,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998993,
                        "timestamp": 1751500800
                      },
                      {
                        "close": 0.999849,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999399,
                        "timestamp": 1751587200
                      },
                      {
                        "close": 0.999735,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999354,
                        "timestamp": 1751673600
                      },
                      {
                        "close": 0.999606,
                        "currency_code": "USD",
                        "high": 0.999904,
                        "low": 0.999077,
                        "timestamp": 1751760000
                      },
                      {
                        "close": 0.999887,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998904,
                        "timestamp": 1751846400
                      },
                      {
                        "close": 0.9998,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999447,
                        "timestamp": 1751932800
                      },
                      {
                        "close": 0.999636,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998979,
                        "timestamp": 1752019200
                      },
                      {
                        "close": 0.999512,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999187,
                        "timestamp": 1752105600
                      },
                      {
                        "close": 0.999537,
                        "currency_code": "USD",
                        "high": 0.999945,
                        "low": 0.99905,
                        "timestamp": 1752192000
                      },
                      {
                        "close": 0.999581,
                        "currency_code": "USD",
                        "high": 0.999886,
                        "low": 0.999098,
                        "timestamp": 1752278400
                      },
                      {
                        "close": 0.999651,
                        "currency_code": "USD",
                        "high": 0.999773,
                        "low": 0.999141,
                        "timestamp": 1752364800
                      },
                      {
                        "close": 0.999694,
                        "currency_code": "USD",
                        "high": 0.999785,
                        "low": 0.998938,
                        "timestamp": 1752451200
                      },
                      {
                        "close": 0.999647,
                        "currency_code": "USD",
                        "high": 0.99996,
                        "low": 0.998674,
                        "timestamp": 1752537600
                      },
                      {
                        "close": 0.999773,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999115,
                        "timestamp": 1752624000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999152,
                        "timestamp": 1752710400
                      },
                      {
                        "close": 0.999678,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999431,
                        "timestamp": 1752796800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999597,
                        "timestamp": 1752883200
                      },
                      {
                        "close": 0.999532,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999223,
                        "timestamp": 1752969600
                      },
                      {
                        "close": 0.99965,
                        "currency_code": "USD",
                        "high": 0.99994,
                        "low": 0.99927,
                        "timestamp": 1753056000
                      },
                      {
                        "close": 0.999762,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.9995,
                        "timestamp": 1753142400
                      },
                      {
                        "close": 0.999745,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999279,
                        "timestamp": 1753228800
                      },
                      {
                        "close": 0.999351,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999302,
                        "timestamp": 1753315200
                      },
                      {
                        "close": 0.999906,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998862,
                        "timestamp": 1753401600
                      },
                      {
                        "close": 0.999759,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999341,
                        "timestamp": 1753488000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999234,
                        "timestamp": 1753574400
                      },
                      {
                        "close": 0.999935,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999058,
                        "timestamp": 1753660800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999073,
                        "timestamp": 1753747200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999035,
                        "timestamp": 1753833600
                      },
                      {
                        "close": 0.999331,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999041,
                        "timestamp": 1753920000
                      },
                      {
                        "close": 0.999742,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998673,
                        "timestamp": 1754006400
                      },
                      {
                        "close": 0.999513,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998953,
                        "timestamp": 1754092800
                      },
                      {
                        "close": 0.999652,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999081,
                        "timestamp": 1754179200
                      },
                      {
                        "close": 0.999372,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998819,
                        "timestamp": 1754265600
                      },
                      {
                        "close": 0.999867,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998779,
                        "timestamp": 1754352000
                      },
                      {
                        "close": 0.999742,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999058,
                        "timestamp": 1754438400
                      },
                      {
                        "close": 0.999908,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998825,
                        "timestamp": 1754524800
                      },
                      {
                        "close": 0.999777,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999011,
                        "timestamp": 1754611200
                      },
                      {
                        "close": 0.999611,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999235,
                        "timestamp": 1754697600
                      },
                      {
                        "close": 0.999598,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99895,
                        "timestamp": 1754784000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998937,
                        "timestamp": 1754870400
                      },
                      {
                        "close": 0.999705,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999029,
                        "timestamp": 1754956800
                      },
                      {
                        "close": 0.999506,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999129,
                        "timestamp": 1755043200
                      },
                      {
                        "close": 0.999782,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99919,
                        "timestamp": 1755129600
                      },
                      {
                        "close": 0.99976,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999279,
                        "timestamp": 1755216000
                      },
                      {
                        "close": 0.999932,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999546,
                        "timestamp": 1755302400
                      },
                      {
                        "close": 0.999958,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999562,
                        "timestamp": 1755388800
                      },
                      {
                        "close": 0.999863,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999513,
                        "timestamp": 1755475200
                      },
                      {
                        "close": 0.999872,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999591,
                        "timestamp": 1755561600
                      },
                      {
                        "close": 0.999845,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999379,
                        "timestamp": 1755648000
                      },
                      {
                        "close": 0.999484,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999302,
                        "timestamp": 1755734400
                      },
                      {
                        "close": 0.99963,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999121,
                        "timestamp": 1755820800
                      },
                      {
                        "close": 0.999578,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999216,
                        "timestamp": 1755907200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999247,
                        "timestamp": 1755993600
                      },
                      {
                        "close": 0.999783,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998956,
                        "timestamp": 1756080000
                      },
                      {
                        "close": 0.999906,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999215,
                        "timestamp": 1756166400
                      },
                      {
                        "close": 0.999837,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999131,
                        "timestamp": 1756252800
                      },
                      {
                        "close": 0.999465,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999072,
                        "timestamp": 1756339200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998987,
                        "timestamp": 1756425600
                      },
                      {
                        "close": 0.999448,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999349,
                        "timestamp": 1756512000
                      },
                      {
                        "close": 0.999408,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999248,
                        "timestamp": 1756598400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999212,
                        "timestamp": 1756684800
                      },
                      {
                        "close": 0.999702,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999196,
                        "timestamp": 1756771200
                      },
                      {
                        "close": 0.999858,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999277,
                        "timestamp": 1756857600
                      },
                      {
                        "close": 0.999709,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999229,
                        "timestamp": 1756944000
                      },
                      {
                        "close": 0.999724,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999132,
                        "timestamp": 1757030400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.998964,
                        "timestamp": 1757116800
                      },
                      {
                        "close": 0.999965,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999444,
                        "timestamp": 1757203200
                      },
                      {
                        "close": 0.999804,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.99921,
                        "timestamp": 1757289600
                      },
                      {
                        "close": 0.99985,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999349,
                        "timestamp": 1757376000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999157,
                        "timestamp": 1757462400
                      },
                      {
                        "close": 0.999871,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999017,
                        "timestamp": 1757548800
                      },
                      {
                        "close": 0.999924,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999302,
                        "timestamp": 1757635200
                      },
                      {
                        "close": 0.999793,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999428,
                        "timestamp": 1757721600
                      },
                      {
                        "close": 0.999763,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999603,
                        "timestamp": 1757808000
                      },
                      {
                        "close": 0.999843,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999357,
                        "timestamp": 1757894400
                      },
                      {
                        "close": 0.999837,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999452,
                        "timestamp": 1757980800
                      },
                      {
                        "close": 0.999759,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999174,
                        "timestamp": 1758067200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998666,
                        "timestamp": 1758153600
                      },
                      {
                        "close": 0.999878,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998049,
                        "timestamp": 1758240000
                      },
                      {
                        "close": 0.999783,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998635,
                        "timestamp": 1758326400
                      },
                      {
                        "close": 0.999783,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999345,
                        "timestamp": 1758412800
                      },
                      {
                        "close": 0.999736,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999073,
                        "timestamp": 1758499200
                      },
                      {
                        "close": 0.99988,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998516,
                        "timestamp": 1758585600
                      },
                      {
                        "close": 0.999861,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998455,
                        "timestamp": 1758672000
                      },
                      {
                        "close": 0.999899,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.997671,
                        "timestamp": 1758758400
                      },
                      {
                        "close": 0.999737,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.997598,
                        "timestamp": 1758844800
                      },
                      {
                        "close": 0.99967,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.999386,
                        "timestamp": 1758931200
                      },
                      {
                        "close": 0.999996,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.999423,
                        "timestamp": 1759017600
                      },
                      {
                        "close": 0.999812,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.997591,
                        "timestamp": 1759104000
                      },
                      {
                        "close": 0.999759,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.997367,
                        "timestamp": 1759190400
                      },
                      {
                        "close": 0.999929,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99726,
                        "timestamp": 1759276800
                      },
                      {
                        "close": 0.999761,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999165,
                        "timestamp": 1759363200
                      },
                      {
                        "close": 0.999703,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999306,
                        "timestamp": 1759449600
                      },
                      {
                        "close": 0.999861,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999106,
                        "timestamp": 1759536000
                      },
                      {
                        "close": 0.999947,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998487,
                        "timestamp": 1759622400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999115,
                        "timestamp": 1759708800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999038,
                        "timestamp": 1759795200
                      },
                      {
                        "close": 0.999937,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998948,
                        "timestamp": 1759881600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999399,
                        "timestamp": 1759968000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998834,
                        "timestamp": 1760054400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998707,
                        "timestamp": 1760140800
                      },
                      {
                        "close": 0.999948,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999256,
                        "timestamp": 1760227200
                      },
                      {
                        "close": 0.999932,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999409,
                        "timestamp": 1760313600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999421,
                        "timestamp": 1760400000
                      },
                      {
                        "close": 0.999903,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999268,
                        "timestamp": 1760486400
                      },
                      {
                        "close": 0.999696,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999296,
                        "timestamp": 1760572800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999042,
                        "timestamp": 1760659200
                      },
                      {
                        "close": 0.999969,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.9993,
                        "timestamp": 1760745600
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999427,
                        "timestamp": 1760832000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999327,
                        "timestamp": 1760918400
                      },
                      {
                        "close": 0.999815,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999049,
                        "timestamp": 1761004800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99923,
                        "timestamp": 1761091200
                      },
                      {
                        "close": 0.9999,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999364,
                        "timestamp": 1761177600
                      },
                      {
                        "close": 0.999947,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999127,
                        "timestamp": 1761264000
                      },
                      {
                        "close": 0.999872,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999299,
                        "timestamp": 1761350400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999524,
                        "timestamp": 1761436800
                      },
                      {
                        "close": 0.999962,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999389,
                        "timestamp": 1761523200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999103,
                        "timestamp": 1761609600
                      },
                      {
                        "close": 0.999957,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99874,
                        "timestamp": 1761696000
                      },
                      {
                        "close": 0.999724,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999012,
                        "timestamp": 1761782400
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998979,
                        "timestamp": 1761868800
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999334,
                        "timestamp": 1761955200
                      },
                      {
                        "close": 0.999953,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99945,
                        "timestamp": 1762041600
                      },
                      {
                        "close": 0.999845,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998958,
                        "timestamp": 1762128000
                      },
                      {
                        "close": 0.999749,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998511,
                        "timestamp": 1762214400
                      },
                      {
                        "close": 0.999653,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999064,
                        "timestamp": 1762300800
                      },
                      {
                        "close": 0.999621,
                        "currency_code": "USD",
                        "high": 1.002,
                        "low": 0.998328,
                        "timestamp": 1762387200
                      },
                      {
                        "close": 0.999863,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999015,
                        "timestamp": 1762473600
                      },
                      {
                        "close": 0.999961,
                        "currency_code": "USD",
                        "high": 1,
                        "low": 0.999452,
                        "timestamp": 1762560000
                      },
                      {
                        "close": 0.999754,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.99924,
                        "timestamp": 1762646400
                      },
                      {
                        "close": 0.999391,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999242,
                        "timestamp": 1762732800
                      },
                      {
                        "close": 0.999726,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999159,
                        "timestamp": 1762819200
                      },
                      {
                        "close": 0.999418,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998937,
                        "timestamp": 1762905600
                      },
                      {
                        "close": 0.999937,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998893,
                        "timestamp": 1762992000
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998596,
                        "timestamp": 1763078400
                      },
                      {
                        "close": 0.999921,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999132,
                        "timestamp": 1763164800
                      },
                      {
                        "close": 0.99985,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998893,
                        "timestamp": 1763251200
                      },
                      {
                        "close": 1,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998753,
                        "timestamp": 1763337600
                      },
                      {
                        "close": 0.999973,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998451,
                        "timestamp": 1763424000
                      },
                      {
                        "close": 0.999529,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.999168,
                        "timestamp": 1763510400
                      },
                      {
                        "close": 0.999601,
                        "currency_code": "USD",
                        "high": 1.001,
                        "low": 0.998835,
                        "timestamp": 1763596800
                      }
                    ]
                  }
                },
                "metrics": null,
                "price": {
                  "change": -0.0003509999999999902,
                  "change_percent": -0.0003511081413075656,
                  "currency_code": "USD",
                  "extended_change": null,
                  "extended_change_percent": null,
                  "extended_price": null,
                  "intraday_high": 1.001,
                  "intraday_low": 0.998303,
                  "intraday_volume": null,
                  "latest_trade_timestamp": null,
                  "market_status": "Open",
                  "open_price": null,
                  "price": 0.999341
                }
              },
              "ticker": "PYUSD",
              "type": "stock",
              "url": null,
              "user_time_zone": "America/New_York"
            },
            {
              "alt": null,
              "end_idx": 261,
              "invalid": true,
              "matched_text": "citeturn0finance0",
              "prompt_text": null,
              "refs": [],
              "safe_urls": [],
              "start_idx": 241,
              "type": "hidden"
            },
            {
              "alt": "([CoinMarketCap](https://coinmarketcap.com/currencies/paypal-usd/?utm_source=chatgpt.com))",
              "end_idx": 430,
              "error": null,
              "fallback_items": null,
              "items": [
                {
                  "attribution": "CoinMarketCap",
                  "attribution_segments": null,
                  "attributions": null,
                  "hue": null,
                  "pub_date": null,
                  "refs": [
                    {
                      "ref_index": 0,
                      "ref_type": "search",
                      "turn_index": 0
                    },
                    {
                      "ref_index": 1,
                      "ref_type": "search",
                      "turn_index": 0
                    }
                  ],
                  "snippet": "PayPal USD is down 0.02% in the last 24 hours. The current CoinMarketCap ranking is #29, with a live market cap of $3,610,397,754 USD. It has a circulating ...",
                  "supporting_websites": [
                    {
                      "attribution": "Coinbase",
                      "pub_date": null,
                      "snippet": "PayPal USD (PYUSD) Price USD Today is $1.00. News, predictions, charts, market cap, buy, sell, convert, and invest on the most trusted platform for crypto.",
                      "title": "PayPal USD Price, PYUSD Price, Live Charts, and Marketcap",
                      "url": "https://www.coinbase.com/price/paypal-usd?utm_source=chatgpt.com"
                    }
                  ],
                  "title": "PayPal USD price PYUSD #29",
                  "url": "https://coinmarketcap.com/currencies/paypal-usd/?utm_source=chatgpt.com"
                }
              ],
              "matched_text": "citeturn0search0turn0search1",
              "prompt_text": null,
              "refs": [],
              "safe_urls": [
                "https://coinmarketcap.com/currencies/paypal-usd/",
                "https://coinmarketcap.com/currencies/paypal-usd/?utm_source=chatgpt.com",
                "https://www.coinbase.com/price/paypal-usd",
                "https://www.coinbase.com/price/paypal-usd?utm_source=chatgpt.com"
              ],
              "start_idx": 398,
              "status": "done",
              "style": null,
              "type": "grouped_webpages"
            },
            {
              "alt": "([Messari](https://messari.io/project/pyusd?utm_source=chatgpt.com))",
              "end_idx": 639,
              "error": null,
              "fallback_items": null,
              "items": [
                {
                  "attribution": "Messari",
                  "attribution_segments": null,
                  "attributions": null,
                  "hue": null,
                  "pub_date": null,
                  "refs": [
                    {
                      "ref_index": 2,
                      "ref_type": "search",
                      "turn_index": 0
                    },
                    {
                      "ref_index": 8,
                      "ref_type": "search",
                      "turn_index": 0
                    }
                  ],
                  "snippet": "PayPal USD (PYUSD) saw a significant 22% increase in its market capitalization over the past week, adding $600 million to its circulating supply 1.",
                  "supporting_websites": [
                    {
                      "attribution": "MEXC",
                      "pub_date": null,
                      "snippet": "PYUSD's rapid growth is attributed to PayPal's extensive user base and its strong influence in the fintech industry. What does a $1 billion market cap mean in ...",
                      "title": "PYUSD Market Cap Exceeds $1 Billion: Will It Ignite the ...",
                      "url": "https://www.mexc.com/learn/article/pyusd-market-cap-exceeds-1-billion-will-it-ignite-the-crypto-market-/1?utm_source=chatgpt.com"
                    }
                  ],
                  "title": "PayPal USD Price, PYUSD to USD, Research, News & ...",
                  "url": "https://messari.io/project/pyusd?utm_source=chatgpt.com"
                }
              ],
              "matched_text": "citeturn0search2turn0search8",
              "prompt_text": null,
              "refs": [],
              "safe_urls": [
                "https://messari.io/project/pyusd",
                "https://messari.io/project/pyusd?utm_source=chatgpt.com",
                "https://www.mexc.com/learn/article/pyusd-market-cap-exceeds-1-billion-will-it-ignite-the-crypto-market-/1",
                "https://www.mexc.com/learn/article/pyusd-market-cap-exceeds-1-billion-will-it-ignite-the-crypto-market-/1?utm_source=chatgpt.com"
              ],
              "start_idx": 607,
              "status": "done",
              "style": null,
              "type": "grouped_webpages"
            },
            {
              "alt": "([PayPal](https://www.paypal.com/us/digital-wallet/manage-money/crypto/pyusd?utm_source=chatgpt.com))",
              "end_idx": 817,
              "error": null,
              "fallback_items": null,
              "items": [
                {
                  "attribution": "PayPal",
                  "attribution_segments": null,
                  "attributions": null,
                  "hue": null,
                  "pub_date": null,
                  "refs": [
                    {
                      "ref_index": 5,
                      "ref_type": "search",
                      "turn_index": 0
                    }
                  ],
                  "snippet": "PYUSD is a stablecoin pegged 1:1 to USD, backed by US dollar deposits, and can be bought/sold on PayPal. Holding it may earn rewards.",
                  "supporting_websites": [],
                  "title": "PYUSD Stablecoin | US Dollar Crypto Rewards",
                  "url": "https://www.paypal.com/us/digital-wallet/manage-money/crypto/pyusd?utm_source=chatgpt.com"
                }
              ],
              "matched_text": "citeturn0search5",
              "prompt_text": null,
              "refs": [],
              "safe_urls": [
                "https://www.paypal.com/us/digital-wallet/manage-money/crypto/pyusd",
                "https://www.paypal.com/us/digital-wallet/manage-money/crypto/pyusd?utm_source=chatgpt.com"
              ],
              "start_idx": 798,
              "status": "done",
              "style": null,
              "type": "grouped_webpages"
            },
            {
              "alt": "([arXiv](https://arxiv.org/abs/2508.02403?utm_source=chatgpt.com))",
              "end_idx": 944,
              "error": null,
              "fallback_items": null,
              "items": [
                {
                  "attribution": "arXiv",
                  "attribution_segments": null,
                  "attributions": null,
                  "hue": null,
                  "pub_date": null,
                  "refs": [
                    {
                      "ref_index": 11,
                      "ref_type": "academia",
                      "turn_index": 0
                    },
                    {
                      "ref_index": 12,
                      "ref_type": "search",
                      "turn_index": 0
                    }
                  ],
                  "snippet": "",
                  "supporting_websites": [
                    {
                      "attribution": "Wikipedia",
                      "pub_date": null,
                      "snippet": "",
                      "title": "Stablecoin",
                      "url": "https://de.wikipedia.org/wiki/Stablecoin?utm_source=chatgpt.com"
                    }
                  ],
                  "title": "SoK: Stablecoins for Digital Transformation -- Design, Metrics, and Application with Real World Asset Tokenization as a Case Study",
                  "url": "https://arxiv.org/abs/2508.02403?utm_source=chatgpt.com"
                }
              ],
              "matched_text": "citeturn0academia11turn0search12",
              "prompt_text": null,
              "refs": [],
              "safe_urls": [
                "https://arxiv.org/abs/2508.02403",
                "https://arxiv.org/abs/2508.02403?utm_source=chatgpt.com",
                "https://de.wikipedia.org/wiki/Stablecoin",
                "https://de.wikipedia.org/wiki/Stablecoin?utm_source=chatgpt.com"
              ],
              "start_idx": 908,
              "status": "done",
              "style": null,
              "type": "grouped_webpages"
            },
            {
              "alt": "([arXiv](https://arxiv.org/abs/2508.02403?utm_source=chatgpt.com))",
              "end_idx": 2087,
              "error": null,
              "fallback_items": null,
              "items": [
                {
                  "attribution": "arXiv",
                  "attribution_segments": null,
                  "attributions": null,
                  "hue": null,
                  "pub_date": null,
                  "refs": [
                    {
                      "ref_index": 11,
                      "ref_type": "academia",
                      "turn_index": 0
                    }
                  ],
                  "snippet": "",
                  "supporting_websites": [],
                  "title": "SoK: Stablecoins for Digital Transformation -- Design, Metrics, and Application with Real World Asset Tokenization as a Case Study",
                  "url": "https://arxiv.org/abs/2508.02403?utm_source=chatgpt.com"
                }
              ],
              "matched_text": "citeturn0academia11",
              "prompt_text": null,
              "refs": [],
              "safe_urls": [
                "https://arxiv.org/abs/2508.02403",
                "https://arxiv.org/abs/2508.02403?utm_source=chatgpt.com"
              ],
              "start_idx": 2065,
              "status": "done",
              "style": null,
              "type": "grouped_webpages"
            },
            {
              "alt": "",
              "end_idx": 3091,
              "has_images": false,
              "matched_text": " ",
              "prompt_text": null,
              "refs": [],
              "safe_urls": [],
              "sources": [
                {
                  "attribution": "CoinMarketCap",
                  "title": "PayPal USD price PYUSD #29",
                  "url": "https://coinmarketcap.com/currencies/paypal-usd/?utm_source=chatgpt.com"
                },
                {
                  "attribution": "Messari",
                  "title": "PayPal USD Price, PYUSD to USD, Research, News & ...",
                  "url": "https://messari.io/project/pyusd?utm_source=chatgpt.com"
                },
                {
                  "attribution": "PayPal",
                  "title": "PYUSD Stablecoin | US Dollar Crypto Rewards",
                  "url": "https://www.paypal.com/us/digital-wallet/manage-money/crypto/pyusd?utm_source=chatgpt.com"
                },
                {
                  "attribution": "arXiv",
                  "title": "SoK: Stablecoins for Digital Transformation -- Design, Metrics, and Application with Real World Asset Tokenization as a Case Study",
                  "url": "https://arxiv.org/abs/2508.02403?utm_source=chatgpt.com"
                }
              ],
              "start_idx": 3091,
              "type": "sources_footnote"
            }
          ],
          "default_model_slug": "gpt-5-1-thinking",
          "finish_details": {
            "stop_tokens": [
              200002
            ],
            "type": "stop"
          },
          "is_complete": true,
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "ef00d2db-7b81-4921-9406-acdf852d24f0",
          "request_id": "68f6df39-6ff0-4267-a5bc-79b130c89c99",
          "safe_urls": [
            "https://arxiv.org/abs/2508.02403",
            "https://arxiv.org/abs/2508.02403?utm_source=chatgpt.com",
            "https://coinmarketcap.com/currencies/paypal-usd/",
            "https://coinmarketcap.com/currencies/paypal-usd/?utm_source=chatgpt.com",
            "https://de.wikipedia.org/wiki/Stablecoin",
            "https://de.wikipedia.org/wiki/Stablecoin?utm_source=chatgpt.com",
            "https://messari.io/project/pyusd",
            "https://messari.io/project/pyusd?utm_source=chatgpt.com",
            "https://www.coinbase.com/price/paypal-usd",
            "https://www.coinbase.com/price/paypal-usd?utm_source=chatgpt.com",
            "https://www.mexc.com/learn/article/pyusd-market-cap-exceeds-1-billion-will-it-ignite-the-crypto-market-/1",
            "https://www.mexc.com/learn/article/pyusd-market-cap-exceeds-1-billion-will-it-ignite-the-crypto-market-/1?utm_source=chatgpt.com",
            "https://www.paypal.com/us/digital-wallet/manage-money/crypto/pyusd",
            "https://www.paypal.com/us/digital-wallet/manage-money/crypto/pyusd?utm_source=chatgpt.com"
          ],
          "search_result_groups": [
            {
              "domain": "coinbase.com",
              "entries": [
                {
                  "attribution": "coinbase.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 1,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "PayPal USD (PYUSD) Price USD Today is $1.00. News, predictions, charts, market cap, buy, sell, convert, and invest on the most trusted platform for crypto.",
                  "title": "PayPal USD Price, PYUSD Price, Live Charts, and Marketcap",
                  "type": "search_result",
                  "url": "https://www.coinbase.com/price/paypal-usd?utm_source=chatgpt.com"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "okx.com",
              "entries": [
                {
                  "attribution": "okx.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 3,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "Sep 28, 2025 — With its market capitalization surging from $498 million to $1 billion in 2025, PYUSD is gaining traction among retail users, institutions, and ...",
                  "title": "PYUSD Market Growth: How PayPal's Stablecoin is ...",
                  "type": "search_result",
                  "url": "https://www.okx.com/learn/pyusd-market-growth-paypal-stablecoin?utm_source=chatgpt.com"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "yahoo.com",
              "entries": [
                {
                  "attribution": "yahoo.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 4,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "Oct 4, 2025 — PayPal's PYUSD Stablecoin Tops $1 Billion Market Cap After Spark Partnership · What The Partnership Means · How PayPal Benefits From Its ...",
                  "title": "PayPal's PYUSD Stablecoin Tops $1 Billion Market Cap ...",
                  "type": "search_result",
                  "url": "https://finance.yahoo.com/news/paypals-pyusd-stablecoin-tops-1-154543932.html?utm_source=chatgpt.com"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "gate.com",
              "entries": [
                {
                  "attribution": "gate.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 6,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "7 days ago — As of 2025, PYUSD's market capitalization has reached $3.41 billion, with a circulating supply of approximately 3,408,934,195 tokens, ...",
                  "title": "2025 PYUSD Price Prediction: Analyzing Potential Growth ...",
                  "type": "search_result",
                  "url": "https://www.gate.com/crypto-wiki/article/2025-pyusd-price-prediction-analyzing-potential-growth-and-market-trends-for-the-emerging-stablecoin-20251114?utm_source=chatgpt.com"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "coingecko.com",
              "entries": [
                {
                  "attribution": "coingecko.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 7,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "Sep 24, 2025 — PYUSD joins a stablecoin market that has grown to almost $300 billion in total value, with these digital dollars becoming essential ...",
                  "title": "What Is PayPal USD (PYUSD)? Complete Guide to ...",
                  "type": "search_result",
                  "url": "https://www.coingecko.com/learn/what-is-paypal-usd-pyusd?utm_source=chatgpt.com"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "mexc.com",
              "entries": [
                {
                  "attribution": "mexc.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 8,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "PYUSD's rapid growth is attributed to PayPal's extensive user base and its strong influence in the fintech industry. What does a $1 billion market cap mean in ...",
                  "title": "PYUSD Market Cap Exceeds $1 Billion: Will It Ignite the ...",
                  "type": "search_result",
                  "url": "https://www.mexc.com/learn/article/pyusd-market-cap-exceeds-1-billion-will-it-ignite-the-crypto-market-/1?utm_source=chatgpt.com"
                }
              ],
              "type": "search_result_group"
            },
            {
              "domain": "kraken.com",
              "entries": [
                {
                  "attribution": "kraken.com",
                  "pub_date": null,
                  "ref_id": {
                    "ref_index": 9,
                    "ref_type": "search",
                    "turn_index": 0
                  },
                  "snippet": "The circulating supply of PayPal USD is 3,611,904,340 PYUSD and the current PayPal USD market cap is $3,611,904,340. 114,427,378 PYUSD was purchased today on ...",
                  "title": "PayPal USD price today - PYUSD price chart & live trends",
                  "type": "search_result",
                  "url": "https://www.kraken.com/prices/paypal-usd?utm_source=chatgpt.com"
                }
              ],
              "type": "search_result_group"
            }
          ],
          "timestamp_": "absolute",
          "turn_exchange_id": "9341c883-9f35-49b7-86b4-214248540d60"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": 1763709118.732228,
        "weight": 1
      },
      "parent": "ef00d2db-7b81-4921-9406-acdf852d24f0"
    },
    "b5305836-4a8e-4565-ad00-dc022118e1e2": {
      "children": [
        "d1ed3186-2fa8-4ce7-a214-e5c7d06bdaa7"
      ],
      "id": "b5305836-4a8e-4565-ad00-dc022118e1e2",
      "message": {
        "author": {
          "metadata": {
            "real_author": "tool:web.run"
          },
          "name": "web.run",
          "role": "tool"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            "【turn1calculator0】 1+1 = 2"
          ]
        },
        "create_time": 1763709353.8625486,
        "end_turn": null,
        "id": "b5305836-4a8e-4565-ad00-dc022118e1e2",
        "metadata": {
          "can_save": false,
          "classifier_response": "default",
          "debug_sonic_thread_id": "thread_6920114988e0832b8df16cb6eba7fbfd",
          "default_model_slug": "gpt-5-1-thinking",
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "63d804b7-959a-4b0c-92df-66e118b6ccf2",
          "reasoning_status": "is_reasoning",
          "reasoning_title": "Explaining exchanges, self-custody, and PYUSD options",
          "request_id": "8abc0dc4-a4f8-4ae7-9ff3-ea70afb360f4",
          "timestamp_": "absolute",
          "turn_exchange_id": "b7bee0ab-6241-419b-af89-b98e46e4b067"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "63d804b7-959a-4b0c-92df-66e118b6ccf2"
    },
    "c195d156-76f4-4be6-ba59-c5554fe5fc98": {
      "children": [
        "0ca56f04-7635-4d51-9f12-828731bfd1a9"
      ],
      "id": "c195d156-76f4-4be6-ba59-c5554fe5fc98",
      "message": null,
      "parent": null
    },
    "d03f0aba-e1a1-45f4-b72c-bede2efcc881": {
      "children": [
        "85a5b013-b485-41ed-9886-3e4e27ddf291"
      ],
      "id": "d03f0aba-e1a1-45f4-b72c-bede2efcc881",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "system"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            ""
          ]
        },
        "create_time": 1763709072.4575708,
        "end_turn": null,
        "id": "d03f0aba-e1a1-45f4-b72c-bede2efcc881",
        "metadata": {
          "can_save": false,
          "command": "prompt",
          "contextual_answers_message_type": "sources_and_filters_prompt",
          "default_model_slug": "gpt-5-1-thinking",
          "is_contextual_answers_system_message": true,
          "is_visually_hidden_from_conversation": true,
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "0cc50489-5ba0-42da-ab2e-35130f2ae6d0",
          "request_id": "68f6df39-6ff0-4267-a5bc-79b130c89c99",
          "timestamp_": "absolute",
          "turn_exchange_id": "9341c883-9f35-49b7-86b4-214248540d60"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "0cc50489-5ba0-42da-ab2e-35130f2ae6d0"
    },
    "d1ed3186-2fa8-4ce7-a214-e5c7d06bdaa7": {
      "children": [
        "d32129b7-c238-4d1a-a5c7-2163495dd7a1"
      ],
      "id": "d1ed3186-2fa8-4ce7-a214-e5c7d06bdaa7",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": null,
        "content": {
          "content": "Thought for 14s",
          "content_type": "reasoning_recap"
        },
        "create_time": 1763709354.900038,
        "end_turn": false,
        "id": "d1ed3186-2fa8-4ce7-a214-e5c7d06bdaa7",
        "metadata": {
          "can_save": false,
          "default_model_slug": "gpt-5-1-thinking",
          "finished_duration_sec": 14,
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "b5305836-4a8e-4565-ad00-dc022118e1e2",
          "reasoning_status": "reasoning_ended",
          "request_id": "8abc0dc4-a4f8-4ae7-9ff3-ea70afb360f4",
          "timestamp_": "absolute",
          "turn_exchange_id": "b7bee0ab-6241-419b-af89-b98e46e4b067"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "b5305836-4a8e-4565-ad00-dc022118e1e2"
    },
    "d32129b7-c238-4d1a-a5c7-2163495dd7a1": {
      "children": [],
      "id": "d32129b7-c238-4d1a-a5c7-2163495dd7a1",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": "final",
        "content": {
          "content_type": "text",
          "parts": [
            "Got you. Let me de-mystify this without bullshit.\n\n### 1. What the hell is an “exchange”?\n\nThink of an exchange like:\n\n- A **crypto pawn shop / bank hybrid** where:\n  - You deposit money (cash or crypto)\n  - You trade it for other coins or back to dollars\n  - They hold your balance in an account\n\nExamples (just so you have names in your head): Coinbase, Kraken, Binance, etc.\n\nYou log in → see a balance → click buttons to buy/sell. That’s it on the surface.\n\n### 2. Where your $50 PYUSD probably is\n\nRight now your $50 PYUSD is most likely in one of these:\n\n1. **PayPal/Venmo app**\n   - Then PayPal is acting as the “exchange” for you.\n   - You don’t see blockchains, wallets, or keys. It’s just numbers on a screen.\n\n2. **A centralized exchange (CEX)** like Coinbase, Kraken, etc.\n   - Same idea: you see a balance on their app/website.\n   - They control the underlying crypto; you just have an IOU on their system.\n\n3. **Your own wallet** (Metamask, Phantom, Ledger, etc.)\n   - Then *you* are the bank.\n   - You hold the private keys; nobody can touch it unless they get your seed phrase.\n\nSince you said you “know nothing of exchange,” you’re probably in bucket 1 or 2, not self-custody.\n\n### 3. What you actually need to do with $50 PYUSD\n\nBlunt truth: with $50, you don’t need to overcomplicate this.\n\nYou basically have three sane options:\n\n1. **Use it as a learning toy**\n   - Leave it where it is.\n   - Poke around the app and learn:\n     - How to view your balance\n     - How to send a tiny amount (like $1–2) to another wallet or back to dollars\n   - Treat it as “tuition money” for understanding how this stuff works.\n\n2. **Use it like a stable $50 bill**\n   - Just let it sit as a stablecoin.\n   - If the platform offers a safe yield (like basic savings, nothing crazy like 50% APY), you can park it there.\n   - Don’t chase ridiculous returns. If something sounds degen as hell, assume it’s rigged against you.\n\n3. **Eventually learn exchanges later**\n   - When/if you want to:\n     - Open a reputable exchange account (Coinbase/Kraken type)\n     - Move a small chunk of PYUSD there\n     - Learn how to:\n       - Swap PYUSD → another coin (BTC, ETH, etc.)\n       - Swap back to dollars\n   - Only move *small* amounts until you’re comfortable.\n\n### 4. Stuff to absolutely avoid right now\n\nSince you’re new:\n\n- Don’t:\n  - Give your **seed phrase** or password to anyone. Ever.\n  - Connect your wallet to random websites promising crazy yields.\n  - Take loans, margin, or “leverage trading.” That’s how people nuke accounts.\n  - Dump your entire savings into this because some influencer said “PYUSD is the future.”\n\nFor $50, the smart move is: use it to learn, not to gamble.\n\n---\n\nIf you tell me *which app or platform* you bought the PYUSD on (PayPal, Venmo, Coinbase, etc.), I can walk you through:\n\n- What that platform actually is (exchange vs wallet vs payments app)\n- The exact buttons to tap if you ever want to:\n  - Cash back out to dollars  \n  - Move it somewhere else  \n  - Or just keep it parked safely and forget about it"
          ]
        },
        "create_time": 1763709353.884735,
        "end_turn": true,
        "id": "d32129b7-c238-4d1a-a5c7-2163495dd7a1",
        "metadata": {
          "can_save": true,
          "citations": [],
          "content_references": [
            {
              "alt": "",
              "end_idx": 3047,
              "has_images": false,
              "matched_text": " ",
              "prompt_text": null,
              "refs": [],
              "safe_urls": [],
              "sources": [],
              "start_idx": 3047,
              "type": "sources_footnote"
            }
          ],
          "default_model_slug": "gpt-5-1-thinking",
          "finish_details": {
            "stop_tokens": [
              200002
            ],
            "type": "stop"
          },
          "is_complete": true,
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "d1ed3186-2fa8-4ce7-a214-e5c7d06bdaa7",
          "request_id": "8abc0dc4-a4f8-4ae7-9ff3-ea70afb360f4",
          "safe_urls": [],
          "timestamp_": "absolute",
          "turn_exchange_id": "b7bee0ab-6241-419b-af89-b98e46e4b067"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": 1763709378.225965,
        "weight": 1
      },
      "parent": "d1ed3186-2fa8-4ce7-a214-e5c7d06bdaa7"
    },
    "e0b0481b-ecd4-4b17-a4d9-c1e15673d2c3": {
      "children": [
        "244753b4-4903-42d8-8f58-dc3d9a62026e"
      ],
      "id": "e0b0481b-ecd4-4b17-a4d9-c1e15673d2c3",
      "message": {
        "author": {
          "metadata": {
            "real_author": "tool:web.run"
          },
          "name": "web.run",
          "role": "tool"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            "【turn0finance0】 PayPal USD (PYUSD) is a crypto in the CRYPTO market. The price is 0.999341 USD currently with a change of -0.00035 (-0.00035%) from the previous close. The intraday high is 1.001 USD and the intraday low is 0.998303 USD."
          ]
        },
        "create_time": 1763709081.655237,
        "end_turn": null,
        "id": "e0b0481b-ecd4-4b17-a4d9-c1e15673d2c3",
        "metadata": {
          "can_save": false,
          "classifier_response": "default",
          "debug_sonic_thread_id": "thread_69201098ec60832d8eaee17daa4b481c",
          "default_model_slug": "gpt-5-1-thinking",
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "acb17a99-2de5-4ef7-8332-3c950369d371",
          "reasoning_status": "is_reasoning",
          "request_id": "68f6df39-6ff0-4267-a5bc-79b130c89c99",
          "timestamp_": "absolute",
          "turn_exchange_id": "9341c883-9f35-49b7-86b4-214248540d60"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "acb17a99-2de5-4ef7-8332-3c950369d371"
    },
    "ef00d2db-7b81-4921-9406-acdf852d24f0": {
      "children": [
        "b4f8bbb2-b834-4ee6-9bfc-76df7002124f"
      ],
      "id": "ef00d2db-7b81-4921-9406-acdf852d24f0",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "assistant"
        },
        "channel": null,
        "content": {
          "content": "Thought for 24s",
          "content_type": "reasoning_recap"
        },
        "create_time": 1763709097.873254,
        "end_turn": false,
        "id": "ef00d2db-7b81-4921-9406-acdf852d24f0",
        "metadata": {
          "can_save": false,
          "default_model_slug": "gpt-5-1-thinking",
          "finished_duration_sec": 24,
          "message_type": "next",
          "model_slug": "gpt-5-1-thinking",
          "parent_id": "2ac9cc41-8064-4f5b-86f6-391fc7818886",
          "reasoning_status": "reasoning_ended",
          "request_id": "68f6df39-6ff0-4267-a5bc-79b130c89c99",
          "timestamp_": "absolute",
          "turn_exchange_id": "9341c883-9f35-49b7-86b4-214248540d60"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "2ac9cc41-8064-4f5b-86f6-391fc7818886"
    },
    "fb3e71b2-1e27-458a-9574-b09b40f9323c": {
      "children": [
        "63d804b7-959a-4b0c-92df-66e118b6ccf2"
      ],
      "id": "fb3e71b2-1e27-458a-9574-b09b40f9323c",
      "message": {
        "author": {
          "metadata": {},
          "name": null,
          "role": "user"
        },
        "channel": null,
        "content": {
          "content_type": "text",
          "parts": [
            "I know nothing if exchange"
          ]
        },
        "create_time": 1763709339.801292,
        "end_turn": null,
        "id": "fb3e71b2-1e27-458a-9574-b09b40f9323c",
        "metadata": {
          "can_save": false,
          "dictation": false,
          "message_source": null,
          "request_id": "8abc0dc4-a4f8-4ae7-9ff3-ea70afb360f4",
          "timestamp_": "absolute",
          "triggered_by_system_hint_suggestion": false,
          "turn_exchange_id": "b7bee0ab-6241-419b-af89-b98e46e4b067"
        },
        "recipient": "all",
        "status": "finished_successfully",
        "update_time": null,
        "weight": 1
      },
      "parent": "aa768706-b869-41ed-8bc8-0c662f57de44"
    }
  },
  "memory_scope": "global_enabled",
  "moderation_results": [],
  "title": "PYUSD growth potential",
  "update_time": 1763835682.373001,
  "voice": null
}
```
