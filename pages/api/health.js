export default async function handler(req, res) {
  try {
    res.status(200).json({ status: 'healthy', model: 'groq-chat-1', tools: ['search','code','calculate','files'] });
  } catch (err) {
    res.status(500).json({ status: 'error', error: err.message });
  }
}
