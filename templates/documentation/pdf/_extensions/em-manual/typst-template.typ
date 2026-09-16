// Original Engineering Method layout. Quarto supplies document conversion,
// callouts, cross-references and brand-color through its standard template.
#let em-manual(
  title: [], subtitle: [], lang: "en", font: ("Helvetica Neue",),
  font-size: 11pt, code-font: ("Menlo",), code-size: 9pt, show-toc: true,
  toc-title: [], toc-depth: 2, numbering-pattern: "1.1",
  accent: rgb("007D8A"), ink: rgb("20262B"), muted: rgb("5C6873"), body,
) = {
  let german = lang.starts-with("de")
  set document(title: title)
  set text(font: font, size: font-size, fill: ink, lang: lang)
  set par(justify: false, leading: 0.65em, spacing: 0.9em)
  set heading(numbering: numbering-pattern)
  set page(
    footer: context [
      #line(length: 100%, stroke: 0.4pt + accent.lighten(70%))
      #v(2mm)
      #set text(size: 8pt, fill: muted)
      #grid(columns: (1fr, auto), gutter: 5mm,
        title, [
          #if german { [Seite] } else { [Page] }
          #counter(page).get().first()
          #if german { [von] } else { [of] }
          #counter(page).final().first()
        ])
    ],
  )
  show link: set text(fill: accent)
  show raw: set text(font: code-font, size: code-size)
  set table(
    inset: 5pt,
    stroke: 0.4pt + accent.lighten(70%),
    fill: (x, y) => if y == 0 { accent.lighten(94%) } else { none },
  )
  show table.cell.where(y: 0): set text(weight: "bold")
  show heading.where(level: 1): it => {
    if it.numbering != none { pagebreak(weak: true) }
    block(above: 5mm, below: 4mm, width: 100%)[
      #set text(size: 20pt, weight: "bold")
      #if it.numbering != none {
        box(fill: accent, radius: 3pt, inset: (x: 7pt, y: 3pt))[
          #text(fill: white, size: 14pt, counter(heading).display(it.numbering))
        ]
        h(7pt)
      }
      #it.body
      #v(2mm)
      #line(length: 100%, stroke: 0.5pt + accent.lighten(70%))
    ]
  }
  show heading.where(level: 2): set text(size: 14pt, weight: "bold")
  show heading.where(level: 3): set text(size: 11pt, weight: "bold")
  show quote.where(block: true): it => block(
    width: 100%, inset: 10pt, fill: accent.lighten(93%),
    stroke: (left: 2pt + accent), it.body,
  )
  line(length: 100%, stroke: 2pt + accent)
  v(5mm)
  text(size: 9pt, weight: "bold", fill: accent,
    if german { "DOKUMENTATION" } else { "DOCUMENTATION" })
  v(3mm)
  text(size: 28pt, weight: "bold", title)
  v(2mm)
  text(size: 12pt, fill: muted, subtitle)
  v(8mm)
  if show-toc {
    outline(
      title: if toc-title != [] { toc-title } else if german { [Inhaltsverzeichnis] } else { [Contents] },
      depth: toc-depth, indent: 1em,
    )
    v(5mm)
  }
  body
}
