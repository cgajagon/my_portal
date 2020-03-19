from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView

from my_portal.tooling import models, forms, views

class AuditFlow(Flow):
    """
    Audit Tool Condition
    """
    process_class = models.ToolConditionProcess

    start = flow.Start(
        CreateProcessView,
        fields=["tool_inspected"],
        task_title="New Audit"
    ).Permission(
        'audit.create_audit'
    ).Next(this.perform_audit)

    perform_audit = flow.View(
        views.ToolConditionProcessCreateView
    ).Assign(
        lambda act:act.process.created_by
    ).Next(this.approve)

    approve = flow.View(
        UpdateProcessView,
        form_class=forms.ApproveForm,
        task_title="Approve",
    ).Assign(
        lambda act:act.process.created_by
    ).Next(this.check_approve)

    check_approve = flow.If(
        cond=lambda act: act.process.approved
    ).Then(this.end).Else(this.perform_audit)

    end = flow.End()