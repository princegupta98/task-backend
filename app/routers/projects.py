from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app import models, schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_or_404(project_id: int, db: Session, user_id: int) -> models.Project:
    project = (
        db.query(models.Project)
        .filter(models.Project.id == project_id, models.Project.owner_id == user_id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/", response_model=List[schemas.ProjectResponse])
def list_projects(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    projects = (
        db.query(models.Project)
        .filter(models.Project.owner_id == current_user.id)
        .options(joinedload(models.Project.tasks))
        .all()
    )
    for p in projects:
        p.task_count = len(p.tasks)
    return projects


@router.post(
    "/", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED
)
def create_project(
    payload: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    project = models.Project(**payload.model_dump(), owner_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    project.task_count = 0
    return project


@router.get("/recent-tasks", tags=["Tasks"])
def get_recent_tasks(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tasks = (
        db.query(models.Task)
        .join(models.Project)
        .filter(models.Project.owner_id == current_user.id)
        .options(joinedload(models.Task.project))
        .order_by(models.Task.created_at.desc())
        .limit(limit)
        .all()
    )
    result = []
    for task in tasks:
        result.append(
            schemas.TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                project_id=task.project_id,
                project_title=task.project.title,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
        )
    return result


@router.get("/{project_id}", response_model=schemas.ProjectWithTasks)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == project_id, models.Project.owner_id == current_user.id
        )
        .options(joinedload(models.Project.tasks))
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.task_count = len(project.tasks)
    return project


@router.put("/{project_id}", response_model=schemas.ProjectResponse)
def update_project(
    project_id: int,
    payload: schemas.ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    project = get_project_or_404(project_id, db, current_user.id)

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    project.task_count = len(project.tasks)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    project = get_project_or_404(project_id, db, current_user.id)
    db.delete(project)
    db.commit()
