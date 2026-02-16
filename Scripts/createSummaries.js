// --- CONFIGURATION ---
const listFileName = "TagSummaries/KeyTags.md"; // Full path to your list file
const summaryFolderName = "TagSummaries";      // Folder where files should be created
const scriptPath = "Scripts/tag_summary";        // Path to your tagSummary script

// --- SCRIPT START ---
const listPage = dv.page(listFileName);

if (!listPage) {
    dv.paragraph(`❌ **Error:** Could not find the list file at: \`${listFileName}\``);
} else {
    // Extracting texts from bullet points
    const keytags = listPage.file.lists.map(li => li.text.trim()).filter(t => t.length > 0);
    
    if (keytags.length === 0) {
        dv.paragraph("⚠️ **No words found** in the bullet list of " + listFileName);
    } else {
        dv.header(3, "Processing Keytags...");
        
        // 1. Ensure the destination folder exists
        const folderExists = app.vault.getAbstractFileByPath(summaryFolderName);
        if (!folderExists) {
            dv.paragraph(`📁 Creating folder: \`${summaryFolderName}\`...`);
            await app.vault.createFolder(summaryFolderName);
        }

        // 2. Loop through each word and create files
        for (let tag of keytags) {
            const fileName = `Target word '${tag}'`;
            const filePath = `${summaryFolderName}/${fileName}.md`;
            
            const existingFile = app.vault.getAbstractFileByPath(filePath);

            if (!existingFile) {
                const content = `\`\`\`dataviewjs\nawait dv.view("${scriptPath}", { word: "${tag}" })\n\`\`\``;
                
                try {
                    await app.vault.create(filePath, content);
                    dv.paragraph(`✅ Created: **${fileName}**`);
                } catch (err) {
                    dv.paragraph(`❌ Failed to create **${fileName}**: ${err}`);
                }
            } else {
                dv.paragraph(`ℹ️ Skipped (already exists): **${fileName}**`);
            }
        }
        dv.paragraph("🏁 **Done!**");
    }
}
