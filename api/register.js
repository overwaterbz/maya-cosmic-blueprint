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
    const { fullName, email, password, birthDate, birthTime, birthLocation } = req.body;

    if (!fullName || !email || !password || !birthDate) {
      return res.status(400).json({ detail: 'Name, email, password, and birth date required' });
    }

    // Create demo Maya cosmic profile - matches documented baseline
    const mayaProfile = {
      full_name: fullName,
      email: email,
      birth_date: birthDate,
      birth_time: birthTime || '12:00',
      birth_location: birthLocation || 'Unknown',
      day_sign: 'Ahau',
      galactic_tone: 'Spectral',
      element: 'Fire',
      direction: 'East',
      kin_number: 260,
      color_family: 'Yellow',
      tribe: 'Sun',
      guide_sign: 'Etznab',
      antipode_sign: 'Men',
      occult_sign: 'Cib',
      spirit_animal: 'Eagle',
      crystal_ally: 'Citrine',
      plant_medicine: 'Sage',
      chakra_resonance: 'Crown',
      human_design_type: 'Manifestor'
    };
    
    const token = 'demo-jwt-token-' + Date.now();
    
    return res.status(200).json({
      token: token,
      message: 'Registration successful',
      maya_profile: mayaProfile
    });

  } catch (error) {
    console.error('Registration error:', error);
    return res.status(500).json({ detail: 'Internal server error' });
  }
}