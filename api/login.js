module.exports = async (req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  if (req.method !== 'POST') {
    return res.status(405).json({ detail: 'Method not allowed' });
  }

  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ detail: 'Email and password required' });
    }

    // Demo authentication 
    const token = 'demo-jwt-' + Date.now();
    
    return res.status(200).json({
      token: token,
      message: 'Login successful'
    });

  } catch (error) {
    return res.status(500).json({ detail: 'Login failed' });
  }
};