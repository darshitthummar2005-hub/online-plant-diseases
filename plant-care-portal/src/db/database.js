import Dexie from 'dexie'
import { seedDiseases, seedPlants } from './seed.js'

export const db = new Dexie('greenroot_db')

db.version(1).stores({
  diseases: '++id, name, type, severity, updatedAt',
  plants: '++id, name, family, updatedAt',
  posts: '++id, author, text, likes, createdAt',
  threads: '++id, title, author, replies, views, createdAt',
  comments: '++id, postId, author, text, createdAt',
})

export async function ensureSeeded() {
  const postCount = await db.posts.count()
  const threadCount = await db.threads.count()

  // Upsert seed rows by name so existing installs are upgraded in place
  // (e.g. when the offline knowledge base grows from 12 to 50+ diseases).
  await seedByName(db.diseases, seedDiseases, 'disease')
  await seedByName(db.plants, seedPlants, 'plant')

  if (postCount === 0) await db.posts.bulkAdd(seedPosts())
  if (threadCount === 0) await db.threads.bulkAdd(seedThreads())

  return {
    diseaseCount: await db.diseases.count(),
    plantCount: await db.plants.count(),
  }
}

async function seedByName(table, seeds, label) {
  const existing = await table.toArray()
  const byName = new Map(existing.map((row) => [String(row.name).toLowerCase(), row]))
  let added = 0
  let updated = 0

  for (const seed of seeds) {
    const current = byName.get(String(seed.name).toLowerCase())
    if (current) {
      const { id, ...rest } = current
      const next = { ...rest, ...seed, updatedAt: current.updatedAt ?? Date.now() }
      await table.update(id, next)
      updated += 1
    } else {
      await table.add({ ...seed, updatedAt: Date.now() })
      added += 1
    }
  }

  if (added || updated) {
    console.info(`[seed] ${label}s: ${added} added, ${updated} updated`)
  }
}

function seedPosts() {
  return [
    {
      author: 'Priya Garden',
      text: 'My tomato plants finally fruited after 90 days of patient care! 🍅 The neem oil spray totally fixed the aphid issue.',
      likes: 24,
      createdAt: Date.now() - 1000 * 60 * 60 * 2,
      comments: [],
    },
    {
      author: 'GreenFingers Raj',
      text: 'Tip of the day: water deeply but rarely. Shallow watering makes weak roots that can\'t reach down for nutrients.',
      likes: 41,
      createdAt: Date.now() - 1000 * 60 * 60 * 26,
      comments: [],
    },
    {
      author: 'Sofia Blooms',
      text: 'Just rescued a monstera from the curb! Three yellow leaves later, it\'s thriving in indirect light. 🌿',
      likes: 18,
      createdAt: Date.now() - 1000 * 60 * 60 * 50,
      comments: [],
    },
    {
      author: 'Leaf Doctor',
      text: 'Wondering why your leaves are curling? Check the undersides — spider mites leave tiny webs and speckles.',
      likes: 33,
      createdAt: Date.now() - 1000 * 60 * 60 * 74,
      comments: [],
    },
    {
      author: 'Basil Buddy',
      text: 'Basil tip: pinch off flowers as soon as they appear. It keeps the leaves bushy and flavorful all season!',
      likes: 29,
      createdAt: Date.now() - 1000 * 60 * 60 * 98,
      comments: [],
    },
  ]
}

function seedThreads() {
  const now = Date.now()
  return [
    {
      title: 'Best organic fungicide for powdery mildew on roses?',
      author: 'RoseQueen',
      replies: 12,
      views: 340,
      createdAt: now - 1000 * 60 * 60 * 5,
    },
    {
      title: 'Seed swap thread 🌱 — share what you have!',
      author: 'SeedSwapper',
      replies: 48,
      views: 980,
      createdAt: now - 1000 * 60 * 60 * 30,
    },
    {
      title: 'How do I revive an overwatered peace lily?',
      author: 'NewbieNana',
      replies: 9,
      views: 215,
      createdAt: now - 1000 * 60 * 60 * 55,
    },
    {
      title: 'Vertical garden ideas for a tiny balcony',
      author: 'CityGrower',
      replies: 21,
      views: 460,
      createdAt: now - 1000 * 60 * 60 * 80,
    },
    {
      title: 'Why are my chili leaves turning yellow between the veins?',
      author: 'SpiceMan',
      replies: 7,
      views: 190,
      createdAt: now - 1000 * 60 * 60 * 110,
    },
  ]
}
