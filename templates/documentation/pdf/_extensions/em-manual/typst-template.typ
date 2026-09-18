// Original Engineering Method layout. Quarto supplies document conversion,
// callouts, cross-references and brand-color through its standard template.
#let em-manual(
  title: [], subtitle: [], lang: "en", font: ("Helvetica Neue",),
  font-size: 12pt, code-font: ("Menlo",), code-size: 9.5pt, show-toc: true,
  toc-title: [], toc-depth: 2, numbering-pattern: "1.1",
  accent: rgb("173A5E"), ink: rgb("232A31"), muted: rgb("5B6670"), body,
) = {
  let german = lang.starts-with("de")
  set document(title: title)
  set text(font: font, size: font-size, fill: ink, lang: lang)
  set par(justify: false, leading: 0.62em, spacing: 0.62em)
  set heading(numbering: numbering-pattern)
  set page(
    footer: context {
      if counter(page).get().first() > 1 [
        #line(length: 100%, stroke: 0.45pt + accent.lighten(64%))
        #v(2.2mm)
        #set text(size: 8.2pt, fill: muted)
        #grid(columns: (1fr, auto), gutter: 5mm,
          title, [
            #if german { [Seite] } else { [Page] }
            #counter(page).get().first()
            #if german { [von] } else { [of] }
            #counter(page).final().first()
          ])
      ]
    },
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
    block(above: 2mm, below: 5.5mm, width: 100%, sticky: true)[
      #stack(
        dir: ttb,
        spacing: 3mm,
        [
          #set text(size: 25pt, weight: "bold")
          #if it.numbering != none {
            text(fill: accent, weight: "regular", counter(heading).display(it.numbering))
            h(9pt)
          }
          #it.body
        ],
        line(length: 100%, stroke: 1pt + accent),
      )
    ]
  }
  show heading.where(level: 2): set text(size: 15pt, weight: "bold", fill: accent)
  show heading.where(level: 2): set block(above: 10pt, below: 4pt, sticky: true)
  show heading.where(level: 3): set text(size: 11.5pt, weight: "bold")
  show heading.where(level: 3): set block(above: 8pt, below: 3pt, sticky: true)
  show quote.where(block: true): it => block(
    width: 100%, inset: 10pt, fill: accent.lighten(93%),
    stroke: (left: 2pt + accent), it.body,
  )
  line(length: 100%, stroke: 2.2pt + accent)
  v(10mm)
  text(size: 9pt, weight: "bold", tracking: 0.08em, fill: accent,
    if german { "DOKUMENTATION" } else { "DOCUMENTATION" })
  v(7mm)
  block(width: 88%)[
    #set par(leading: 0.18em)
    #text(size: 36pt, weight: "bold", title)
  ]
  v(5mm)
  line(length: 34mm, stroke: 1pt + accent)
  v(5mm)
  block(width: 78%)[#text(size: 15pt, fill: muted, subtitle)]
  pagebreak(weak: false)
  if show-toc {
    {
      show outline.entry.where(level: 1): set block(above: 0.75em)
      show outline.entry.where(level: 1): set text(weight: "bold")
      show outline.entry.where(level: 2): set text(size: 10pt, fill: muted)
      outline(
        title: if toc-title != [] { toc-title } else if german { [Inhaltsverzeichnis] } else { [Contents] },
        depth: toc-depth, indent: 1.15em,
      )
    }
    v(7mm)
  }
  body
}
