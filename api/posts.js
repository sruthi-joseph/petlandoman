// api/posts.js
export default async function handler(req, res) {
    // Allow CORS and prevent caching
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');

    const projectId = process.env.NEXT_PUBLIC_SANITY_PROJECT_ID || '1dvvzwi3';
    const dataset = process.env.NEXT_PUBLIC_SANITY_DATASET || 'production';
    const apiVersion = 'v2022-03-07';
    
    const query = `*[_type == "post"] | order(publishedAt desc) {
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
    }`;

    // Fetch directly from live Sanity API (useCdn is false as we query api.sanity.io directly)
    const url = `https://${projectId}.api.sanity.io/${apiVersion}/data/query/${dataset}?query=${encodeURIComponent(query)}`;

    try {
        const response = await fetch(url, {
            headers: process.env.SANITY_API_TOKEN ? {
                'Authorization': `Bearer ${process.env.SANITY_API_TOKEN}`
            } : {},
            cache: 'no-store'
        });
        const data = await response.json();
        
        if (!response.ok) {
            return res.status(response.status).json(data);
        }
        
        return res.status(200).json(data);
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
}
