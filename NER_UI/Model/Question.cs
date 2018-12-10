using System.Collections.Generic;

namespace NER_UI.Model
{
    public class Question
    {
        public Question(string question, List<Answer> answers)
        {
            QuestionText = question;
            Answers = answers;
            isAnswered = false;
        }
        public string QuestionText { get; }
        public List<Answer> Answers { get;}
        public bool isAnswered { get; set; }
    }
}