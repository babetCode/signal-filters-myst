// content/strip-terms.mjs
const isTermRef = (n) =>
  ['crossReference', 'link', 'term'].includes(n.type) &&
  /(^|#)term-/.test(String(n.identifier ?? n.label ?? n.url ?? ''));

function walk(node) {
  if (!node.children) return;
  const out = [];
  for (const child of node.children) {
    walk(child);
    if (child.type === 'glossary') {
      out.push(...(child.children ?? [])); // keep definitions, drop wrapper
    } else {
      if (isTermRef(child)) {
        child.type = 'span'; // keep visible text, drop the link
        for (const k of ['url', 'identifier', 'label', 'kind', 'resolved']) delete child[k];
      }
      out.push(child);
    }
  }
  node.children = out;
}

const plugin = {
  name: 'Strip glossary links for PDF',
  transforms: [
    {
      name: 'strip-glossary-for-pdf',
      stage: 'document',
      plugin: () => (tree) => {
        if (process.env.MYST_PDF) walk(tree);
      },
    },
  ],
};
export default plugin;