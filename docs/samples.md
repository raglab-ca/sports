<!-- Hand-maintained example file for scripts/export-public-docs.js. -->

# Sample responses

Abridged examples of the MCP result envelope. Every tool returns the same
shape — `schemaVersion`, `data`, `meta`, `evidence` — and list tools add
`meta.pagination`. Arrays are truncated here for readability; live responses
carry full rows and fresher timestamps.

See [`developers.md`](developers.md) for connection setup and
[`tools.md`](tools.md) for every tool and parameter.

## `get_power_rankings` — current power snapshot

```json
{
  "schemaVersion": "1.0.0",
  "data": {
    "season": 20262027,
    "asOf": "2026-09-30",
    "teams": [
      {
        "rank": 1,
        "code": "VGK",
        "name": "Vegas Golden Knights",
        "score": 387,
        "deltaDay": 108.2,
        "deltaWeek": 30.8,
        "deltaMonth": 30.8,
        "rankDeltaDay": 7,
        "rankDeltaWeek": 0,
        "rankDeltaMonth": 0
      },
      {
        "rank": 2,
        "code": "VAN",
        "name": "Vancouver Canucks",
        "score": 343,
        "deltaDay": -10.8,
        "deltaWeek": 21.6,
        "deltaMonth": 21.6,
        "rankDeltaDay": -1,
        "rankDeltaWeek": 5,
        "rankDeltaMonth": 5
      }
    ]
  },
  "meta": {
    "serverVersion": "2.1.0",
    "generatedAt": "2026-09-30T14:22:05.114Z",
    "season": 20262027,
    "asOf": "2026-09-30",
    "source": "postgres:power_history",
    "completeness": "complete",
    "modelVersion": null,
    "warnings": [
      "Stored power rows are not model-version stamped; the model version for this snapshot is unknown."
    ]
  },
  "evidence": [
    {
      "id": "power-history:20262027:2026-09-30",
      "type": "power_snapshot",
      "source": "postgres:power_history",
      "season": 20262027,
      "asOf": "2026-09-30"
    }
  ]
}
```

Notes: `score` is snapshot-relative and descriptive, not a win probability.
`delta*`/`rankDelta*` are score and rank changes over 1 day, 7 days, and 30
days. `modelVersion` is null for stored history.

## `get_games` — stored cards for one date

```json
{
  "schemaVersion": "1.0.0",
  "data": {
    "season": 20262027,
    "date": "2026-09-30",
    "games": [
      {
        "id": 2026020001,
        "date": "2026-09-30",
        "startTime": "2026-09-30T23:00:00Z",
        "label": "today",
        "status": "scheduled",
        "away": { "code": "PIT", "name": "Pittsburgh Penguins", "logo": "https://assets.nhle.com/logos/nhl/svg/PIT_light.svg", "score": null },
        "home": { "code": "PHI", "name": "Philadelphia Flyers", "logo": "https://assets.nhle.com/logos/nhl/svg/PHI_light.svg", "score": null },
        "wentOt": false,
        "shootout": false,
        "winner": null,
        "odds": {
          "model": { "away": 118, "home": -138 },
          "market": { "away": 105, "home": -125 }
        },
        "value": {
          "tier": "watch",
          "away": { "evPct": 1.4, "price": 105 },
          "home": { "evPct": -2.1, "price": -125 }
        },
        "edges": { "away": 2.3, "home": -2.3, "tie": null },
        "winProbability": { "away": 0.432, "home": 0.568 },
        "otProbability": 0.214,
        "expectedScore": { "away": 2.61, "home": 3.12 },
        "simulation": null
      }
    ]
  },
  "meta": {
    "serverVersion": "2.1.0",
    "generatedAt": "2026-09-30T14:23:11.902Z",
    "season": 20262027,
    "asOf": "2026-09-30T14:20:00.000Z",
    "source": "postgres:game_cards",
    "completeness": "complete",
    "modelVersion": "2.1.0",
    "warnings": []
  },
  "evidence": [
    {
      "id": "game-cards:20262027:2026-09-30",
      "type": "game_card_set",
      "source": "postgres:game_cards",
      "season": 20262027,
      "asOf": "2026-09-30T14:20:00.000Z"
    }
  ]
}
```

Notes: `odds.model` and `odds.market` are American prices. `value` carries
model-versus-market expected value for upcoming games only and is null for
final games. Probability fields are model estimates, not guarantees.

## `list_teams` — identity and record

```json
{
  "schemaVersion": "1.0.0",
  "data": {
    "season": 20262027,
    "teams": [
      {
        "code": "MTL",
        "name": "Montreal Canadiens",
        "conference": "East",
        "division": "Atlantic",
        "logo": "https://assets.nhle.com/logos/nhl/svg/MTL_light.svg",
        "record": {
          "gamesPlayed": 3,
          "wins": 2,
          "losses": 1,
          "otLosses": 0,
          "points": 4,
          "pointPct": 0.667,
          "regulationWins": 1,
          "goalFor": 9,
          "goalAgainst": 7,
          "goalDiff": 2
        }
      }
    ]
  },
  "meta": {
    "serverVersion": "2.1.0",
    "generatedAt": "2026-09-30T14:24:00.000Z",
    "season": 20262027,
    "asOf": "2026-09-30T14:24:00.000Z",
    "source": "nhl-official-api:league-snapshot",
    "completeness": "complete",
    "modelVersion": null,
    "warnings": []
  },
  "evidence": [
    {
      "id": "league-snapshot:20262027",
      "type": "league_team_snapshot",
      "source": "nhl-official-api:league-snapshot",
      "season": 20262027,
      "asOf": "2026-09-30T14:24:00.000Z"
    }
  ]
}
```
