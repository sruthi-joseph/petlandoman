import { getCliClient } from 'sanity/cli'
const client = getCliClient()

async function check() {
    console.log("Publishing the puppy draft temporarily to see its behavior...");
    const draft = await client.getDocument('drafts.91c31466-af81-49ea-8df6-5b11b7b5ad36');
    const publishedDoc = { ...draft, _id: '91c31466-af81-49ea-8df6-5b11b7b5ad36', _updatedAt: undefined, _createdAt: undefined, _rev: undefined };
    await client.createOrReplace(publishedDoc);
    
    console.log("Fetching with order(publishedAt desc):");
    const posts = await client.fetch('*[_type == "post"] | order(publishedAt desc){_id, title, publishedAt}');
    console.log(posts);

    console.log("Cleaning up (unpublishing the test puppy post)...");
    await client.delete('91c31466-af81-49ea-8df6-5b11b7b5ad36');
}
check();
