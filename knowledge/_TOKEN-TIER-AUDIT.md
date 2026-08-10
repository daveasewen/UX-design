# Token-tier gate (_STANDARDS.md §1)

**Result:** 0 strict failure(s) · 5 advisory (legacy, not gated).
Migrated three-tier set: 47 token(s).

## Advisory — legacy tokens (consistency, not yet gated)

- primary/border/hover (dark): $value #D61412 != resolve(color/red/700) #BA1110
- badge/background (light): $value #B92F1E != resolve(rag/error) #F6604C
- badge/background (dark): $value #CC4333 != resolve(rag/error) #F6604C
- tabs/badge/background (light): $value #B92F1E != resolve(badge/background) #F6604C
- tabs/badge/background (dark): $value #CC4333 != resolve(badge/background) #F6604C
