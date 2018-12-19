using System.Collections.Generic;

namespace NER_UI.Model
{
    public class Question
    {
        public Question(string question, List<Answer> answers)
        {
            QuestionText = question;
            Answers = answers;
            IsAnswered = false;
        }
        public string QuestionText { get; }
        public List<Answer> Answers { get;}
        public bool IsAnswered { get; set; }
    }
}