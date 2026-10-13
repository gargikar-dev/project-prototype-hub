#!/usr/bin/env python3
"""
Unit and Integration Tests for AI Lead Scoring & Pipeline
"""

import sys
import os
import unittest
import json

# Add scripts directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from ai_lead_scorer import (
    score_buying_intent,
    score_icp_fit,
    evaluate_lead,
)
from marketing_drafter import draft_marketing_response, audit_spam_risk

class TestAILeadEngine(unittest.TestCase):

    def setUp(self):
        self.sample_icp = {
            "icp_name": "B2B SaaS Founders & Tech Decision Makers",
            "target_roles": ["SaaS Founder", "CTO", "Technical Lead"],
            "target_industries": ["B2B SaaS", "Fintech", "Software"],
            "core_pain_points": [
                "Stripe Connect integration complexity and merchant onboarding friction",
                "High SaaS payment processing fees and unexpected chargebacks",
                "Need simple alternative to Stripe or Paddle for collecting customer payments"
            ],
            "competitors": ["Stripe", "Paddle", "LemonSqueezy"],
            "disqualifiers": ["student project", "homework", "crypto casino", "gambling"],
            "product_offering": {
                "name": "DirectPay SaaS",
                "core_value_prop": "Simplified direct payment gateway for software founders without Stripe Connect overhead.",
                "differentiator": "Direct client payouts, zero monthly minimums, 5-minute setup."
            }
        }

    def test_high_intent_prospect(self):
        """Verify that an acute solution request scores high (>75)."""
        post = {
            "id": "post_001",
            "title": "Looking for the best payment service alternative to Stripe Connect",
            "content": "I'm building a SaaS for field-service businesses. We need a simpler alternative to Stripe where each client collects payments directly without complex Connect onboarding and high fees. What do you guys recommend?",
            "url": "https://reddit.com/r/SaaS/comments/post_001",
            "subreddit": "SaaS",
            "author": "tech_founder_99",
            "published": "2026-10-09T10:00:00Z"
        }
        res = evaluate_lead(post, self.sample_icp)
        self.assertFalse(res["is_disqualified"])
        self.assertGreaterEqual(res["intent_score"], 70)
        self.assertGreaterEqual(res["icp_match_score"], 70)
        self.assertGreaterEqual(res["composite_score"], 70)
        self.assertEqual(res["intent_category"], "solution_request")
        self.assertIn("Stripe", res["target_product"])

    def test_disqualified_lead(self):
        """Verify that negative keywords immediately disqualify a lead."""
        post = {
            "id": "post_002",
            "title": "Need payment gateway for crypto casino student project",
            "content": "Building a gambling site for my homework assignment. Looking for free payment gateway.",
            "url": "https://reddit.com/r/SaaS/comments/post_002",
            "subreddit": "SaaS",
            "author": "student_dev",
            "published": "2026-10-09T10:00:00Z"
        }
        res = evaluate_lead(post, self.sample_icp)
        self.assertTrue(res["is_disqualified"])
        self.assertEqual(res["composite_score"], 0)
        self.assertIn("Disqualified", res["disqualification_reason"])

    def test_low_intent_casual_chat(self):
        """Verify that general chatter without buying intent scores low (<50)."""
        post = {
            "id": "post_003",
            "title": "Just sharing some thoughts on coffee and coding",
            "content": "What is everyone's favorite coffee roast while building software on weekends?",
            "url": "https://reddit.com/r/SaaS/comments/post_003",
            "subreddit": "SaaS",
            "author": "weekend_coder",
            "published": "2026-10-09T10:00:00Z"
        }
        res = evaluate_lead(post, self.sample_icp)
        self.assertLess(res["composite_score"], 50)

    def test_marketing_drafter_compliance(self):
        """Verify that marketing drafts adhere to 80/20 rule and maintain low spam risk."""
        lead = {
            "thread_title": "Looking for the best payment service alternative to Stripe Connect",
            "core_problem_summary": "Building a SaaS for field-service businesses. We need a simpler alternative to Stripe where each client collects payments directly.",
            "target_product": "Stripe Connect",
            "intent_category": "solution_request"
        }
        draft = draft_marketing_response(lead, self.sample_icp["product_offering"])
        self.assertTrue(draft["requires_hitl_approval"])
        self.assertIn("DirectPay SaaS", draft["drafted_response"])
        self.assertLess(draft["risk_assessment"]["spam_risk_score"], 0.30)
        self.assertTrue(draft["risk_assessment"]["rule_compliance"])

if __name__ == "__main__":
    unittest.main()
