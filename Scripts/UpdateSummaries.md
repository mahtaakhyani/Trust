```dataviewjs
// --- CONFIGURATION ---
const listFileName = "TagSummaries/KeyTags.md";      // The file with your bullet list
const summaryFolderName = "TagSummaries";            // Where to save the new notes
const scriptPath = "Scripts/tag_summary";             // Path to your tagSummary.js script

// --- MASTER SCRIPT START ---
const listPage = dv.page(listFileName);

if (!listPage) {
    dv.paragraph(`❌ **Error:** Could not find the list file at: \`${listFileName}\``);
} else {
    // Extracting texts from bullet points, filtering empty lines
    const keytags = listPage.file.lists.map(li => li.text.trim()).filter(t => t.length > 0);
    
    // 1. Ensure the destination folder exists
    const folderExists = app.vault.getAbstractFileByPath(summaryFolderName);
    if (!folderExists) { await app.vault.createFolder(summaryFolderName); }

    for (let rawTagInput of keytags) {
        // Clean input for processing: space-separated words = OR logic
        const wordsArray = rawTagInput.replace(/\b(or|and)\b/gi, '').trim().split(/\s+/).filter(w => w.length > 0);

        // 2. Pre-check: EXCLUDE "TagRoutes" folder and count matching items
        let matchingItems = dv.pages().where(p => !p.file.path.includes("TagRoutes")) // <--- ADDED FOLDER FILTER
            .file.lists.where(item => 
                wordsArray.some(word => item.tags.some(t => t.toLowerCase().includes(word.toLowerCase())))
            );
        
        // 3. Check if any results were found before creating the file
        if (matchingItems.length === 0) {
            dv.paragraph(`ℹ️ No entries found for "${rawTagInput}". File creation skipped.`);
            continue; 
        }
        
        // 4. Create the file if we have results
        const fileName = `Target word '${rawTagInput}'`;
        const filePath = `${summaryFolderName}/${fileName}.md`;
        const existingFile = app.vault.getAbstractFileByPath(filePath);

        if (!existingFile) {
            const content = `\`\`\`dataviewjs\nawait dv.view("${scriptPath}", { words: ${JSON.stringify(wordsArray)} })\n\`\`\``;
            await app.vault.create(filePath, content);
            dv.paragraph(`✅ Created: **${fileName}**`);
        } else {
            dv.paragraph(`ℹ️ Skipped (already exists): **${fileName}**`);
        }
    }
    dv.paragraph("🏁 **Done!**");
}


```
