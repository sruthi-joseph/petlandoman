import { getCliClient } from 'sanity/cli'
import fs from 'fs'
import path from 'path'

const client = getCliClient()

const blogPosts = [
    {
        tag: "Grooming",
        date: "2026-06-20T00:00:00Z",
        title: "5 Essential Tips for Grooming Your Dog at Home",
        imagePath: "../../assets/images/extracted_images/card_grooming_blog.png",
        desc: "Regular grooming keeps your dog healthy, clean, and happy. Follow these essential professional-approved tips:\n\n1. **Regular Brushing**: Brush your dog's coat at least 3-4 times a week. This removes loose hair, prevents matting, and distributes natural skin oils for a healthy shine.\n\n2. **Use the Right Tools**: Choose brushes designed for your dog's hair type (slicker brushes for long hair, bristle brushes for short). Never use regular scissors to cut mats; use a proper de-matting tool.\n\n3. **Nail Trimming Safety**: Clip nails regularly. If you hear them clicking on the floor, they are too long. Cut small amounts at a time and avoid the quick (the pink blood vessel).\n\n4. **Dog-Safe Shampoo**: Wash your dog with lukewarm water and always use dog-formulated shampoo. Human products can disrupt their skin pH, causing dryness and irritation.\n\n5. **Positive Reinforcement**: Make grooming enjoyable by offering high-value treats and praise, turning it into a bonding experience."
    },
    {
        tag: "Cat Behavior",
        date: "2026-06-15T00:00:00Z",
        title: "Understanding Your Cat's Body Language",
        imagePath: "../../assets/images/extracted_images/card_cat_blog.png",
        desc: "Cats communicate through subtle body movements. Here is how to understand what your feline companion is telling you:\n\n1. **Decoding Tail Movements**: A tail pointing straight up with a slight curve represents a happy, welcoming cat. A thrashing or thumping tail is a clear warning of irritation, while a puffed-up tail indicates fear.\n\n2. **Ear Positions**: Forward-pointing ears indicate curiosity or interest. Ears flattened backward ('airplane ears') signify fear, anxiety, or aggression.\n\n3. **The Eye Language**: Slow blinking is the ultimate sign of affection, often called a 'cat kiss'. Wide dilated pupils show high excitement, fear, or playfulness.\n\n4. **Whiskers Alignment**: A relaxed cat keeps its whiskers pointed outwards to the sides. Curious cats push whiskers forward, while scared or defensive cats pull them back tightly against their cheeks.\n\n5. **The Mystery of Purring**: Although purring usually means comfort, cats also purr to self-soothe when stressed, sick, or in pain. Check their overall posture to understand their mood."
    },
    {
        tag: "Wellness",
        date: "2026-06-10T00:00:00Z",
        title: "The Importance of Active Play & Exercise",
        imagePath: "../../assets/images/extracted_images/card_puppy_blog.png",
        desc: "Playtime and physical exercise are essential for keeping your pets happy, active, and healthy. Regular physical activity provides significant benefits:\n\n1. **Cardiovascular Health**: Running and active play keep your pet's heart strong and healthy, boosting their overall energy.\n\n2. **Mental Stimulation**: Interactive toys and fetch sessions keep their minds sharp, reducing anxiety and boredom-related behaviors.\n\n3. **Weight Management**: Daily exercise burns calories, helping to prevent pet obesity and associated joint or digestive issues.\n\n4. **Bonding Time**: Shared play strengthens the relationship between you and your pet, building trust and cooperation.\n\n5. **Muscle Tone & Flexibility**: Running, stretching, and jumping preserve muscle strength and support joint mobility as your pets grow."
    },
    {
        tag: "Nutrition",
        date: "2026-06-05T00:00:00Z",
        title: "Transitioning Your Pet to a New Diet Smoothly",
        imagePath: "../../assets/images/extracted_images/card_nutrition_blog.png",
        desc: "Switching your pet's food abruptly can lead to vomiting, diarrhea, and digestive upset. Use this safe, expert-approved 7-day transition guide:\n\n* **Days 1 & 2**: Feed a mix of 75% old food and 25% new food. Check for any digestive changes.\n* **Days 3 & 4**: Increase to a 50/50 ratio of old and new food.\n* **Days 5 & 6**: Serve 25% old food mixed with 75% new food.\n* **Day 7**: Transition completely to 100% new food.\n\n**Pro Tip**: If your pet experiences stomach upset or rejects the new food at any stage, return to the previous mix for a couple of days and slow down the transition speed."
    },
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

async function seed() {
    console.log("Starting seed process...");

    for (const post of blogPosts) {
        console.log(`Processing: ${post.title}`);
        
        // Ensure category exists
        const categoryQuery = `*[_type == "category" && title == $title][0]`;
        let category = await client.fetch(categoryQuery, { title: post.tag });
        if (!category) {
            console.log(`Creating category: ${post.tag}`);
            category = await client.create({
                _type: 'category',
                title: post.tag,
                description: post.tag
            });
        }

        // Upload image
        console.log(`Uploading image from ${post.imagePath}`);
        const imageBuffer = fs.readFileSync(path.resolve(__dirname, post.imagePath));
        const imageAsset = await client.assets.upload('image', imageBuffer, {
            filename: path.basename(post.imagePath)
        });

        // Convert simple markdown-like desc to basic block content
        const blocks = post.desc.split('\\n\\n').map(paragraph => ({
            _type: 'block',
            _key: Math.random().toString(36).substring(7),
            style: 'normal',
            children: [
                {
                    _type: 'span',
                    _key: Math.random().toString(36).substring(7),
                    text: paragraph,
                    marks: []
                }
            ]
        }));

        const doc = {
            _type: 'post',
            title: post.title,
            slug: { _type: 'slug', current: post.title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)+/g, '') },
            publishedAt: post.date,
            categories: [
                { _type: 'reference', _ref: category._id, _key: Math.random().toString(36).substring(7) }
            ],
            mainImage: {
                _type: 'image',
                asset: {
                    _type: 'reference',
                    _ref: imageAsset._id
                }
            },
            body: blocks
        };

        // Check if post already exists
        const existingQuery = `*[_type == "post" && title == $title][0]`;
        const existing = await client.fetch(existingQuery, { title: post.title });
        if (existing) {
            console.log(`Post already exists, skipping: ${post.title}\\n`);
            continue;
        }

        console.log(`Creating post document...`);
        await client.create(doc);
        console.log(`Successfully created: ${post.title}\\n`);
    }

    console.log("Seeding complete!");
}

seed().catch(err => {
    console.error("Error during seeding:", err);
});
