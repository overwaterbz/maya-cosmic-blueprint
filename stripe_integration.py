"""
Stripe Integration for Maya Cosmic Blueprint Platform
Premium spiritual tools monetization with subscription and one-time payment support
"""

import stripe
import os
from datetime import datetime, timedelta
import json

# Initialize Stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

class MayaStripeService:
    """Premium spiritual tools payment processing"""
    
    def __init__(self):
        self.stripe_public_key = os.environ.get("VITE_STRIPE_PUBLIC_KEY")
        
        # Promotional free month settings
        self.promo_active = True  # Set to False after promo period
        self.promo_end_date = "2025-08-12"  # End of free month promo
        
        # Spiritual Tools Marketplace (Premium) pricing (USD cents)
        # Single subscription model - all tools included
        self.subscription_prices = {
            "monthly_subscription": 1100,  # $11.00/month for all tools
            "annual_subscription": 11100   # $111.00/year for all tools (save $21)
        }
        
        # MayanBelize.com event integration
        self.event_packages = {
            "tulum_retreat": 199700,  # $1,997 Tulum spiritual retreat
            "maya_ceremony": 49700,   # $497 Traditional Maya ceremony
            "spiritual_guide": 9700   # $97 Personal spiritual guide session
        }
    
    async def create_subscription(self, plan_type, user_email, user_id):
        """Create Stripe subscription for spiritual tools access"""
        try:
            if plan_type not in self.subscription_prices:
                raise ValueError(f"Invalid plan type: {plan_type}")
            
            # Create or get customer
            customer = await self.get_or_create_customer(user_email, user_id)
            
            # Create subscription
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Spiritual Tools Marketplace Premium',
                            'description': 'Access to all spiritual tools: Maya Oracle, Dream Interpreter, Sacred Rituals'
                        },
                        'unit_amount': self.subscription_prices[plan_type],
                        'recurring': {
                            'interval': 'month' if plan_type == 'monthly_subscription' else 'year'
                        }
                    },
                    'quantity': 1
                }],
                trial_period_days=30 if not self.promo_active else 0,  # 30-day free trial
                metadata={
                    'user_id': user_id,
                    'user_email': user_email,
                    'plan_type': plan_type,
                    'platform': 'maya_cosmic_blueprint'
                }
            )
            
            return {
                'subscription_id': subscription.id,
                'client_secret': subscription.latest_invoice.payment_intent.client_secret,
                'amount': self.subscription_prices[plan_type],
                'plan_type': plan_type,
                'trial_days': 30 if not self.promo_active else 0,
                'success': True
            }
            
        except Exception as e:
            print(f"Subscription creation error: {e}")
            return {'error': str(e), 'success': False}
    
    async def get_or_create_customer(self, user_email, user_id):
        """Get or create Stripe customer"""
        try:
            # Try to find existing customer
            customers = stripe.Customer.list(email=user_email, limit=1)
            
            if customers.data:
                return customers.data[0]
            
            # Create new customer
            customer = stripe.Customer.create(
                email=user_email,
                metadata={'user_id': user_id}
            )
            
            return customer
            
        except Exception as e:
            print(f"Customer creation error: {e}")
            raise e
    
    def get_pricing_display(self):
        """Get pricing information for frontend display"""
        pricing = {}
        
        # Subscription pricing
        for plan_type, price_cents in self.subscription_prices.items():
            pricing[plan_type] = {
                'price_cents': price_cents,
                'price_display': f"${price_cents/100:.2f}",
                'interval': 'month' if plan_type == 'monthly_subscription' else 'year',
                'includes_all_tools': True,
                'available': True
            }
        
        # Promotional status
        pricing['promo_active'] = self.promo_active
        pricing['promo_end_date'] = self.promo_end_date
        pricing['promo_message'] = "🎉 FREE until Aug 12, 2025!" if self.promo_active else ""
        
        # Subscription benefits
        pricing['subscription_benefits'] = [
            "Access to all spiritual tools",
            "Maya Oracle Cards with AI wisdom",
            "Dream Interpreter with Maya symbolism", 
            "Sacred Rituals & Breathwork ceremonies",
            "Personalized cosmic guidance",
            "Unlimited tool usage",
            "Priority customer support"
        ]
        
        # Event packages
        for event_name, price_cents in self.event_packages.items():
            pricing[event_name] = {
                'price_cents': price_cents,
                'price_display': f"${price_cents/100:.2f}",
                'available': True
            }
        
        return pricing
    
    async def verify_payment(self, payment_intent_id):
        """Verify payment completion and grant tool access"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                return {
                    'success': True,
                    'tool_name': intent.metadata.get('tool_name'),
                    'user_id': intent.metadata.get('user_id'),
                    'amount_paid': intent.amount / 100  # Convert from cents
                }
            else:
                return {
                    'success': False,
                    'status': intent.status,
                    'error': 'Payment not completed'
                }
                
        except Exception as e:
            print(f"Payment verification error: {e}")
            return {'error': str(e), 'success': False}
    
    async def create_event_booking(self, event_type, user_email, user_id, event_date=None):
        """Create payment for MayanBelize.com events"""
        try:
            if event_type not in self.event_packages:
                raise ValueError(f"Invalid event: {event_type}")
            
            amount = self.event_packages[event_type]
            
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                metadata={
                    'user_id': user_id,
                    'user_email': user_email,
                    'event_type': event_type,
                    'event_date': event_date or '',
                    'purchase_type': 'maya_event',
                    'platform': 'maya_cosmic_blueprint',
                    'partner': 'mayanbelize.com'
                },
                description=f"Maya Spiritual Event: {event_type.replace('_', ' ').title()}"
            )
            
            return {
                'client_secret': intent.client_secret,
                'amount': amount,
                'event_type': event_type,
                'success': True
            }
            
        except Exception as e:
            print(f"Event booking error: {e}")
            return {'error': str(e), 'success': False}
    
    def get_pricing_display(self):
        """Get formatted pricing for frontend display"""
        return {
            'marketplace_title': 'Spiritual Tools Marketplace (Premium)',
            'promo_active': self.promo_active,
            'promo_message': 'FREE for first month! All spiritual tools unlocked until August 12, 2025' if self.promo_active else None,
            'promo_end_date': self.promo_end_date,
            'tools': {
                'maya_oracle': {
                    'price': '$1.99',
                    'name': 'Maya Oracle Cards',
                    'description': '20 sacred cards with AI-powered ancestral wisdom'
                },
                'dream_interpreter': {
                    'price': '$2.99',
                    'name': 'Dream Interpreter',
                    'description': 'AI-powered dream analysis with Maya symbolism'
                },
                'sacred_rituals': {
                    'price': '$3.99',
                    'name': 'Sacred Rituals & Breathwork',
                    'description': 'Personalized ceremonies & cosmic-aligned practices'
                },
                'ai_companion': {
                    'price': '$4.99',
                    'name': 'AI Spiritual Companion Pro',
                    'description': 'Unlimited daily guidance + ritual planning',
                    'note': 'Basic version free (limited questions)'
                }
            },
            'special_products': {
                'pdf_blueprint': {
                    'price': '$7.77',
                    'name': 'PDF Blueprint Download',
                    'description': 'Professionally styled downloadable cosmic blueprint'
                },
                'gift_blueprint': {
                    'price': '$11.00',
                    'name': 'Gift a Cosmic Blueprint',
                    'description': 'Share the magic - gift a reading to friends'
                }
            },
            'subscriptions': {
                'monthly_subscription': {
                    'price': '$11.11/month',
                    'name': 'Monthly Subscription',
                    'description': 'Unlimited access to all spiritual tools + AI companion'
                },
                'annual_pass': {
                    'price': '$111/year',
                    'name': 'Annual Pass',
                    'description': 'Full year access to premium spiritual marketplace',
                    'savings': '$22.32'
                }
            },
            'events': {
                'tulum_retreat': {
                    'price': '$1,997',
                    'name': 'Tulum Spiritual Retreat',
                    'description': '7-day transformational journey in sacred Tulum'
                },
                'maya_ceremony': {
                    'price': '$497',
                    'name': 'Traditional Maya Ceremony',
                    'description': 'Authentic ceremonial experience with Maya elders'
                },
                'spiritual_guide': {
                    'price': '$97',
                    'name': 'Personal Spiritual Guide',
                    'description': 'One-on-one guidance session with Maya spiritual teacher'
                }
            }
        }

# Global service instance
maya_stripe = MayaStripeService()