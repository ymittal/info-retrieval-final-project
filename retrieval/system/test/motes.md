// Based on Search Engines in IR book (bruce, , we need to restirct the context
// of each term.
//
// ---------- Extracted from book: ----------
// Context restriction and evaluation:
// expression.C1,..,CN
// – matches when the expression appears in all con-
// texts C1 through CN.
// expression.(C1,...,CN)
// – evaluates the expression using the language model
// defined by the concatenation of contexts
// C1...CN within the document.
//
// Examples:
// dog.title
// – matches the term “dog” appearing in a title extent.
// #uw(smith jones).author
// – matches when the two names “smith” and “jones”
// appear in an author extent.
// dog.(title)
// – evaluates the term based on the title language model for the
// document. This means that the estimate of the probability of occurrence
// for dog for a given document will be based on the number of times that the
// word occurs in the title field for that document and will be normalized us-
// ing the number of words in the title rather than the document. Similarly,
// smoothing is done using the probabilities of occurrence in the title field
// over the whole collection.
// #od:1(abraham lincoln).person.(header)
// – builds a language model from all
// of the “header” text in the document and evaluates
// #od:1(abraham lincoln).person
// in that context (i.e., matches only the exact phrase appearing
// within a person extent within the header context).
