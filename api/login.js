export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
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

    // Demo authentication - matches documented baseline
    if (email === 'rick@overwater.com' || email.includes('@')) {
      // Create JWT-like token for demo
      const token = 'demo-jwt-token-' + Date.now();
      
      return res.status(200).json({
        token: token,
        message: 'Login successful',
        user: {
          email: email,
          name: 'Maya User',
          cosmic_signature: 'Ahau Spectral'
        }
      });
    }

    return res.status(401).json({ detail: 'Invalid credentials' });

  } catch (error) {
    console.error('Login error:', error);
    return res.status(500).json({ detail: 'Internal server error' });
  }
}