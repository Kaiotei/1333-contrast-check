# Contrast Check

WCAG contrast ratios plus colour-blind simulation in one small Python script, built to catch low-contrast text on translucent panels.

Built by [Kaiotei](https://github.com/Kaiotei) for [13 <33 Covenant](https://1333covenant.com) and released as one of its open-source apps.

## Features

- WCAG 2 ratio under normal vision, protanopia, deuteranopia and tritanopia (Machado et al. 2009).
- Blends a translucent background over a backdrop before measuring, so you test against the lightest thing behind the panel.
- Batch mode for a whole page of colour pairs.

## Run it

```sh
python contrast-check.py '#322036' '#e0ccf8'
python contrast-check.py '#c4a8e8' '#322036' --alpha 0.88 --over '#ffffff'
python contrast-check.py --file pairs.txt   # "label | fg | bg | alpha | over" per line
```

## Make it yours

AA needs 4.5 for body text and 3.0 for large text (24px+, or 19px+ bold).

**Stack:** Python 3, standard library only.

## License

[AGPL-3.0](LICENSE). You can use, change and build on this. If you run a modified version for others over a network, you must share its source under the same license. Keep the credit to 13 <33 Covenant.

## More from 13 <33 Covenant

[1333-island-world](https://github.com/Kaiotei/1333-island-world) · [1333-changing-room](https://github.com/Kaiotei/1333-changing-room) · [1333-whole-armor](https://github.com/Kaiotei/1333-whole-armor) · [1333-globe](https://github.com/Kaiotei/1333-globe) · [1333-jacobs-ladder](https://github.com/Kaiotei/1333-jacobs-ladder) · [1333-angelhub](https://github.com/Kaiotei/1333-angelhub) · [1333-bible-study](https://github.com/Kaiotei/1333-bible-study) · [1333-moon-calendar](https://github.com/Kaiotei/1333-moon-calendar) · [1333-guestbook](https://github.com/Kaiotei/1333-guestbook) · [1333-chat-widget](https://github.com/Kaiotei/1333-chat-widget)
