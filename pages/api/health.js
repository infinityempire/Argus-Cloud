export default async function handler(req, res) {
  try {
    res.status(200).json({ status: 'healthy', model: 'gpt-4', tools: ['search','code','calculate','files'] });
  } catch (err) {
    res.status(500).json({ status: 'error', error: err.message });
  }
}
