---
name: git-sicherheit
description: "Sicher mit Git in einer Ablage arbeiten: den fremden Arbeitsbaum respektieren, nichts Destruktives ohne Auftrag, Inhalt und Werkzeug getrennt committen. Verwenden bei: committen, Arbeitsbaum aufräumen, mehrere Ablagen gleichzeitig ändern."
---

# Git in einer Ablage

Eine Ablage ist ein Repository wie jedes andere, mit einem Unterschied: Ein
Mensch arbeitet darin parallel in Obsidian, und eine zweite Sitzung womöglich
auch. Was du vorfindest, ist nicht unbedingt von dir.

## Vor dem Ändern

**① `git status --short`, immer zuerst.** Ein Arbeitsbaum, der schon offen
steht, gehört jemand anderem. Ihn in den eigenen Commit zu ziehen macht
hinterher unlesbar, was die eigene Änderung war.

**② Fremde Änderungen bleiben liegen.** Wenn sie im Weg sind, sag das und
frag, statt sie mitzunehmen oder zurückzusetzen.

**③ Kein destruktiver Befehl ohne ausdrücklichen Auftrag.** `reset --hard`,
`clean -fd`, `checkout -- .`, ein erzwungener Push: Jeder davon vernichtet
Arbeit, die niemand wiederbekommt. Der Auftrag muss sie benennen, nicht bloß
zulassen.

## Beim Committen

**Inhalt, Struktur und Werkzeug in getrennte Commits.** Eine Notiz, die
umgeschrieben wird, ein Ordner, der umzieht, und ein Skript, das repariert
wird, sind drei Vorgänge. Zusammen committet ist hinterher keiner davon
einzeln zu lesen oder zurückzunehmen.

**Nur die eigenen Pfade vormerken.** `git add -A` nimmt mit, was danebenliegt,
und in einer Ablage liegt regelmäßig ein Sitzungsprotokoll daneben, das gerade
geschrieben wird.

**Vor dem Commit auf Geheimnisse sehen.** Zugangsdaten, absolute Pfade mit
einem Benutzernamen darin, private Anhänge.

## Mehrere Ablagen

Jede ist ein eigenes Repository mit eigenem Arbeitsbaum, eigenem Remote und
eigener Historie. Ein Commit über zwei Ablagen hinweg gibt es nicht. Was
zusammengehört, wird zweimal committet, und die beiden Nachrichten verweisen
aufeinander.

## Der Push

Ob gepusht wird, sagt der Auftrag. Manche Ablage hat einen `post-commit`-Hook,
der es von selbst tut. Nachsehen in `.git/hooks/` und im Log, das er schreibt.
Ein Hook liegt nicht im Repository und fehlt auf einem frischen Klon.
