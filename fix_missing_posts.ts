import { getCliClient } from 'sanity/cli'
import fs from 'fs'
import path from 'path'

const client = getCliClient()

const missingPosts = [
    {
        tag: "Wellness",
        date: "2026-05-28T00:00:00Z",
        title: "How to Keep Your Pets Hydrated in the Summer",
        imagePath: "../../assets/images/extracted_images/card_dog_summer_blog.png",
        desc: "Oman's summer heat can quickly lead to severe dehydration in pets. Safeguard your furry family members with these hydration strategies:\n\n1. **Abundant Water Stations**: Place multiple clean water bowls around your home. Keep water cool by throwing in fresh ice cubes.\n\n2. **Use Water Fountains**: Flowing water attracts pets. A pet drinking fountain filters water and encourages more frequent drinking.\n\n3. **Increase Wet Food**: Mix wet food or low-sodium bone broths into dry kibble to naturally boost their daily moisture intake.\n\n4. **Walk Safely**: Walk pets only in the early mornings or late evenings. Hot pavements can burn paws and lead to rapid heat exhaustion.\n\n5. **Know the Dehydration Signs**: Look out for dry/sticky gums, extreme panting, lethargy, and loss of skin elasticity. If you suspect heatstroke, seek professional assistance immediately."
    },
    {
        tag: "Training",
        date: "2026-05-20T00:00:00Z",
        title: "Creating a Stress-Free Environment for a New Puppy",
        imagePath: "../../assets/images/extracted_images/card_puppy_blog.png",
        desc: "Moving to a new home can be overwhelming for a young puppy. Create a calm, welcoming environment with these steps:\n\n1. **Establish a Safe Space**: Place a cozy wire crate or playpen in a quiet corner. Fill it with a comfortable bed and safe chew toys to make it their private sanctuary.\n\n2. **Thorough Puppy-Proofing**: Remove reachable hazards, secure loose electrical cords, place toxic houseplants out of reach, and secure cabinet doors.\n\n3. **Set a Reliable Schedule**: Feed, walk, play, and put your puppy to sleep at the exact same times daily. Predictability builds confidence and speeds up potty training.\n\n4. **Calm Introductions**: Introduce the puppy to family members and other pets one-by-one. Keep the environment quiet and free of sudden loud noises.\n\n5. **Patience & Positive Reinforcement**: Puppies learn through repetition and positive rewards. Never punish mistakes; instead, reward successful behaviors with treats and soft praise."
    }
];

async function fix() {
    console.log("Cleaning up broken/draft documents...");
    
    // Find all documents with these titles
    for (const post of missingPosts) {
        const docs = await client.fetch(`*[_type == "post" && title == $title]{_id}`, { title: post.title });
        for (const doc of docs) {
            console.log(`Deleting ${doc._id}`);
            await client.delete(doc._id);
        }
    }
    
    console.log("Seeding missing posts...");
    for (const post of missingPosts) {
        console.log(`Processing: ${post.title}`);
        
        let category = await client.fetch(`*[_type == "category" && title == $title][0]`, { title: post.tag });
        if (!category) {
            category = await client.create({ _type: 'category', title: post.tag, description: post.tag });
        }

        const imageBuffer = fs.readFileSync(path.resolve(__dirname, post.imagePath));
        const imageAsset = await client.assets.upload('image', imageBuffer, { filename: path.basename(post.imagePath) });

        const blocks = post.desc.split('\n\n').map(paragraph => ({
            _type: 'block',
            _key: Math.random().toString(36).substring(7),
            style: 'normal',
            children: [{ _type: 'span', _key: Math.random().toString(36).substring(7), text: paragraph, marks: [] }]
        }));

        const doc = {
            _type: 'post',
            title: post.title,
            slug: { _type: 'slug', current: post.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)+/g, '') },
            publishedAt: post.date,
            categories: [{ _type: 'reference', _ref: category._id, _key: Math.random().toString(36).substring(7) }],
            mainImage: { _type: 'image', asset: { _type: 'reference', _ref: imageAsset._id } },
            body: blocks
        };

        await client.create(doc);
        console.log(`Successfully published: ${post.title}`);
    }
    console.log("All done!");
}
fix();
