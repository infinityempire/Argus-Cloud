// In-memory store; replace with DB for production.
let memories = [];

export default async function handler(req, res) {
  if (req.method === 'GET') {
    return res.status(200).json({ status:'success', memories });
  }
  if (req.method === 'POST') {
    const { question, answer } = req.body || {};
    if (!question || !answer) {
      return res.status(400).json({ status:'error', error:'Missing question or answer' });
    }
    memories.push({ question, answer, timestamp:Date.now() });
    return res.status(201).json({ status:'success' });
  }
  res.setHeader('Allow',['GET','POST']);
  return res.status(405).json({ status:'error', error:`Method ${req.method} Not Allowed` });
}
