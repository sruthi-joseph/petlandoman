import { getCliClient } from 'sanity/cli'
const client = getCliClient()

async function check() {
    const posts = await client.fetch('*[_id in path("drafts.**")]');
    console.log("DRAFTS:");
    posts.forEach(p => console.dir(p, {depth: null}));
}
check();
