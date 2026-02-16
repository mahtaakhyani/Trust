// tagSummary.js (Excluding TagsRoutes)
const targetWords = input.words; 
const targetWordsString = targetWords.join(', ');
const { app } = this; 

let listItems = dv.pages()
    // 1. FILTER: Ignore all files located in the TagRoutes folder
    .where(p => !p.file.path.includes("TagsRoutes"))
    .file.lists
    .where(item => {
        // Use nullish coalescing (?? []) to ensure tags is always an array
        const tags = item.tags ?? []; 
        
        return targetWords.some(word => 
            tags.some(t => {
                // Ensure 't' is a string using optional chaining and nullish coalescing
                const tagName = t?.toLowerCase() ?? '';
                return tagName.includes(word.toLowerCase());
            })
        );
    });

if (listItems.length > 0) {
    dv.header(2, "Summary for: " + targetWordsString);

    for (let group of listItems.groupBy(item => item.path)) {
        // Use nullish coalescing for safety on file path as well
        const filePath = group.key ?? 'Untitled File';
        const fileLink = dv.fileLink(filePath);
        
        dv.paragraph("### " + fileLink);
        
        dv.list(group.rows.map(item => {
            // Ensure item.text is treated safely
            const cleanText = (item.text ?? '').replace(/\s?\^[a-zA-Z0-9-]+$/, "");
            
            // Ensure item.link is handled safely
            const itemLink = item.link ?? '#'; 
            let shortenedLink = item.link.withDisplay(item.link.subpath);
            return cleanText + '\n *' + shortenedLink + '*';
        }));
        dv.paragraph("---");
    }
}
