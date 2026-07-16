const https = require('https');

const projectId = '1dvvzwi3';
const dataset = 'production';
const apiVersion = 'v2022-03-07';
const query = encodeURIComponent(`*[_type == "post"] | order(publishedAt desc) {
    title,
    publishedAt,
    mainImage{
        asset->{
            url
        }
    },
    categories[]->{
        title
    },
    body
}`);
const url = `https://${projectId}.api.sanity.io/${apiVersion}/data/query/${dataset}?query=${query}`;

https.get(url, (res) => {
    let data = '';
    res.on('data', (chunk) => data += chunk);
    res.on('end', () => {
        const parsed = JSON.parse(data);
        const result = parsed.result;
        console.log(`Found ${result.length} posts`);
        
        try {
            result.forEach(post => {
                const category = post.categories && post.categories.length > 0 ? post.categories[0].title : 'Uncategorized';
                const date = new Date(post.publishedAt).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
                
                // This is where it might crash!
                const descText = (post.body || []).map(block => {
                    if (block.children) {
                        return block.children.map(child => child.text).join('');
                    }
                    return ''; // If block.children is missing
                }).join('\n\n');
                
                // Let's check the original code which does: 
                // const descText = (post.body || []).map(block => block.children.map(child => child.text).join('')).join('\n\n');
                // I will run the original code to see if it crashes:
                const descTextOrig = (post.body || []).map(block => block.children.map(child => child.text).join('')).join('\n\n');
                
                console.log(`Success processing: ${post.title}`);
            });
            console.log("All posts processed successfully with original logic!");
        } catch (e) {
            console.error("Crash during processing:", e.message);
        }
    });
});
