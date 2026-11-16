# Bonus HW: Critical Paper Reviews

Read `handout.pdf` first. It has all the rules.

## Files

| File | What it is |
|---|---|
| `handout.pdf` | The rules: points, paper list, review structure, format, submission, grading. |
| `review-template.tex` | The LaTeX template. Write every review in this template. |
| `review-template.pdf` | What the empty template looks like when compiled. |
| `review-template-overleaf.zip` | The same template, ready for Overleaf. |

## The paper list

https://sal-research.github.io/comparch-fall-2026/homeworks.html#bonus-papers

**The list is dynamic.** We add papers as the lectures progress. Check the list before you choose a paper.

## Writing a review

1. Pick a paper from the list. Note its **paper key** (for example, `kim2014flipping`).
2. Copy `review-template.tex`, or use the Overleaf option below.
3. Fill in your name, student ID, paper key, paper title, and venue at the top.
4. Replace the placeholder text in every section with your review.
5. Compile the template. The PDF must have **at most two pages**.
6. Name the PDF `review_<studentID>_<paperkey>.pdf`. Example: `review_22012345_kim2014flipping.pdf`.
7. Upload it to the Moodle assignment "Bonus HW: Paper Reviews".

**Compile locally:**

```
pdflatex review-template.tex
pdflatex review-template.tex
```

Run it twice, so that the page count in the footer is correct.

**Compile on Overleaf:** New Project → Upload Project → choose `review-template-overleaf.zip`.

**Deadline:** December 27, 2026, 23:59 (Ankara time). No late submissions.

**Questions:** [Bonus HW discussion forum](https://github.com/SAL-Research/comparch-fall-2026/discussions/categories/bonus-hw-paper-reviews). Do not post any part of your review there.
