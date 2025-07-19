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
    const { fullName, email, password, birthDate } = req.body;

    if (!fullName || !email || !password || !birthDate) {
      return res.status(400).json({ detail: 'Required fields missing' });
    }

    const token = 'demo-jwt-' + Date.now();
    
    return res.status(200).json({
      token: token,
      message: 'Registration successful',
      maya_profile: {
        fullName,
        email,
        birthDate,
        day_sign: 'Ahau',
        galactic_tone: 'Spectral'
      }
    });

  } catch (error) {
    return res.status(500).json({ detail: 'Registration failed' });
  }
};