from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InterviewSession, Question, Answer
from .ai_service import generate_questions, evaluate_answer

@login_required
def start_interview(request):
    if request.method == "POST":
        category = request.POST.get('category')
        difficulty = request.POST.get('difficulty')
        job_role = request.POST.get('job_role')

        # You can store in DB or session
        request.session['category'] = category
        request.session['difficulty'] = difficulty
        request.session['job_role'] = job_role

        return redirect('interview_page')  # next page

    return render(request, 'interviews/start.html')

@login_required
def interview_question(request, session_id, q_order):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    question = get_object_or_404(Question, session=session, order=q_order)
    total = session.questions.count()

    if request.method == 'POST':
        answer_text = request.POST['answer']
        feedback = evaluate_answer(question.text, answer_text, session.job_role)
        
        # Parse score from feedback (first number found)
        import re
        scores = re.findall(r'\b(\d+(?:\.\d+)?)/10\b', feedback)
        score = float(scores[0]) if scores else None

        Answer.objects.create(
            question=question, text=answer_text,
            ai_feedback=feedback, score=score
        )
        if q_order < total:
            return redirect('interview_question', session_id=session_id, q_order=q_order+1)
        return redirect('interview_results', session_id=session_id)

    return render(request, 'interviews/question.html', {
        'session': session, 'question': question,
        'q_order': q_order, 'total': total
    })

@login_required
def interview_results(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    answers = Answer.objects.filter(question__session=session).select_related('question')
    
    scores = [a.score for a in answers if a.score is not None]
    overall = sum(scores) / len(scores) if scores else 0
    session.overall_score = overall
    session.is_completed = True
    session.save()

    return render(request, 'interviews/results.html', {
        'session': session, 'answers': answers, 'overall': round(overall, 1)
    })

@login_required
def question_view(request):
    questions = request.session.get('questions', [
        "Tell me about yourself",
        "What is Django?",
        "Explain REST API"
    ])

    q_index = request.session.get('q_index', 0)

    if q_index >= len(questions):
        return redirect('result')

    question = questions[q_index]

    return render(request, 'interviews/question.html', {
        'question': question,
        'q_order': q_index + 1,
        'total': len(questions),
        'progress': int(((q_index + 1) / len(questions)) * 100)
    })