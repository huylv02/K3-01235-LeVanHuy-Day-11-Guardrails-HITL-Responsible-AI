"""
Lab 11 — Part 4: Human-in-the-Loop Design
  TODO 11: Confidence Router
  TODO 12: Design 3 HITL decision points
"""
from dataclasses import dataclass


# ============================================================
# TODO 11: Implement ConfidenceRouter
# ============================================================

HIGH_RISK_ACTIONS = [
    "transfer_money",
    "close_account",
    "change_password",
    "delete_data",
    "update_personal_info",
]


@dataclass
class RoutingDecision:
    """Result of the confidence router."""
    action: str          # "auto_send", "queue_review", "escalate"
    confidence: float
    reason: str
    priority: str        # "low", "normal", "high"
    requires_human: bool


class ConfidenceRouter:
    """Route agent responses based on confidence and risk level."""

    HIGH_THRESHOLD = 0.9
    MEDIUM_THRESHOLD = 0.7

    def route(self, response: str, confidence: float,
              action_type: str = "general") -> RoutingDecision:
        """Route a response based on confidence score and action type."""
        
        # 1. Check if action_type is in HIGH_RISK_ACTIONS
        if action_type in HIGH_RISK_ACTIONS:
            return RoutingDecision(
                action="escalate",
                confidence=confidence,
                reason=f"High-risk action: {action_type}",
                priority="high",
                requires_human=True,
            )
        
        # 2. Check confidence thresholds:
        if confidence >= self.HIGH_THRESHOLD:
            return RoutingDecision(
                action="auto_send",
                confidence=confidence,
                reason="High confidence",
                priority="low",
                requires_human=False,
            )
        elif confidence >= self.MEDIUM_THRESHOLD:
            return RoutingDecision(
                action="queue_review",
                confidence=confidence,
                reason="Medium confidence — needs review",
                priority="normal",
                requires_human=True,
            )
        else:
            return RoutingDecision(
                action="escalate",
                confidence=confidence,
                reason="Low confidence — escalating",
                priority="high",
                requires_human=True,
            )


# ============================================================
# TODO 12: Design 3 HITL decision points
# ============================================================

hitl_decision_points = [
    {
        "id": 1,
        "name": "High-Value Transaction Review",
        "trigger": "Transactions exceeding $10,000",
        "hitl_model": "human-in-the-loop",
        "context_needed": "Transaction history, recipient details, user risk profile",
        "example": "User requests transfer of $15,000 to a new account.",
        "approval_path": "Approve to proceed, Reject to block, Timeout to hold for further verification",
        "audit_fields": "Request correlation ID, original transfer intent, reviewer ID and decision",
    },
    {
        "id": 2,
        "name": "Suspicious Account Activity Alert",
        "trigger": "Multiple failed login attempts or unusual access patterns",
        "hitl_model": "human-on-the-loop",
        "context_needed": "Access logs, device fingerprint, historical activity",
        "example": "User logs in from a foreign country after multiple failed attempts.",
        "approval_path": "Approve to unlock, Reject to continue temporary lockout, Timeout to force password reset",
        "audit_fields": "Correlation ID, login activity logs, reviewer action",
    },
    {
        "id": 3,
        "name": "Account Closure Verification",
        "trigger": "Request to close a long-standing banking account",
        "hitl_model": "human-as-tiebreaker",
        "context_needed": "Reason for closure, account balance, retention offer details",
        "example": "Customer requests to close account citing 'poor service'.",
        "approval_path": "Approve to close, Reject to prevent premature closure, Timeout to escalate to customer support",
        "audit_fields": "Correlation ID, account history, retention offer, reviewer decision",
    },
]


# ============================================================
# Quick tests
# ============================================================

def test_confidence_router():
    """Test ConfidenceRouter with sample scenarios."""
    router = ConfidenceRouter()

    test_cases = [
        ("Balance inquiry", 0.95, "general"),
        ("Interest rate question", 0.82, "general"),
        ("Ambiguous request", 0.55, "general"),
        ("Transfer $50,000", 0.98, "transfer_money"),
        ("Close my account", 0.91, "close_account"),
    ]

    print("Testing ConfidenceRouter:")
    print("=" * 80)
    print(f"{'Scenario':<25} {'Conf':<6} {'Action Type':<18} {'Decision':<15} {'Priority':<10} {'Human?'}")
    print("-" * 80)

    for scenario, conf, action_type in test_cases:
        decision = router.route(scenario, conf, action_type)
        print(
            f"{scenario:<25} {conf:<6.2f} {action_type:<18} "
            f"{decision.action:<15} {decision.priority:<10} "
            f"{'Yes' if decision.requires_human else 'No'}"
        )

    print("=" * 80)


def test_hitl_points():
    """Display HITL decision points."""
    print("\nHITL Decision Points:")
    print("=" * 60)
    for point in hitl_decision_points:
        print(f"\n  Decision Point #{point['id']}: {point['name']}")
        print(f"    Trigger:  {point['trigger']}")
        print(f"    Model:    {point['hitl_model']}")
        print(f"    Context:  {point['context_needed']}")
        print(f"    Example:  {point['example']}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_confidence_router()
    test_hitl_points()
