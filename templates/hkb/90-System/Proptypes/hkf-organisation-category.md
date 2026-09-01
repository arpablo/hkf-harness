---
type: proptype
form: text
values:
  - association
  - authority
  - company
  - foundation
  - institute
  - ngo
  - party
  - religious
  - school
  - union
  - university
created: 2026-08-27
modified: 2026-08-31T18:30:00
modified_by: claude-opus-5
---

Art einer Körperschaft. Wird als Listenform
`hkf-organisation-category-list` verwendet, weil eine Körperschaft mehreres
zugleich sein kann — eine Landesuniversität ist `university` und `authority`.

| Wert | Gemeint ist |
|---|---|
| `association` | Verein, Verband, Gesellschaft |
| `authority` | Behörde, Amt, Körperschaft öffentlichen Rechts |
| `company` | erwerbswirtschaftliches Unternehmen |
| `foundation` | Stiftung |
| `institute` | Forschungs- oder Fachinstitut |
| `ngo` | Nichtregierungsorganisation |
| `party` | politische Partei |
| `religious` | Religionsgemeinschaft |
| `school` | Schule, allgemein- oder berufsbildend |
| `union` | Gewerkschaft |
| `university` | Hochschule |

Die Rechtsform gehört nicht hierher, sondern in den Body: `company` sagt
nichts darüber, ob es eine GmbH oder eine AG ist.
