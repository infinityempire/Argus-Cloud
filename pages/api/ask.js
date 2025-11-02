import fetch from 'node-fetch';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow',['POST']);
    return res.status(405).json({ status:'error', error:`Method ${req.method} Not Allowed` });
  }
  const { question } = req.body || {};
  if (!question) return res.status(400).json({ status:'error', error:'Missing question' });

  try {
    const apiKey = process.env.GROQ_API_KEY;
    if (!apiKey) throw new Error('GROQ_API_KEY not configured');
    const response = await fetch('https://api.groq.ai/v1/chat/completions', {
      method:'POST',
      headers:{ 'Content-Type':'application/json', 'Authorization':`Bearer ${apiKey}` },
      body: JSON.stringify({
        model:'groq-chat-1',
        messages:[
          { role:'system', content:'You are Argus, a fully autonomous AI agent capable of performing any digital task.' },
          { role:'user', content:question }
        ]
      })
    });
    if (!response.ok) {
      const errText = await response.text();
      return res.status(response.status).json({ status:'error', error:errText });
    }
    const data = await response.json();
    const answer = data.choices?.[0]?.message?.content?.trim() || '';
    return res.status(200).json({ status:'success', answer });
  } catch (err) {
    res.status(500).json({ status:'error', error:err.message });
  }
}
