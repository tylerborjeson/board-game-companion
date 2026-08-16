# ArkhamDB public API

**Document:** ArkhamDB public API  
**URL:** https://arkhamdb.com/api/  
**Docs:** https://arkhamdb.com/api/doc  
**Lookup:** `scripts/arkham-card <collector-number>`

Authorized **revealed-card** lookup only. Not a campaign guide. Not a dump of the card pool.

When Tyler gives a collector number (for example `141` or `#141`), fetch that card immediately. Do not ask him to read the card first.

```text
scripts/arkham-card 141
GET https://arkhamdb.com/api/public/card/01141
```

A five-digit code is used as-is. A shorter number tries Core (`01` + three digits), then Revised Core / Core pack position.

Use stats, traits, keywords, spawn, victory, and ability text. Honor HTTP cache headers. Do not commit API responses, flavor dumps, or card images.

The physical card still wins. If Tyler reports different text, stop and ask.
