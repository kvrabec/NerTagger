﻿namespace NER_UI.Model
{
    public class Answer
    {
        public Answer(string text, bool isCorrect = false)
        {
            Text = text;
            IsCorrect = isCorrect;
        }
        public string Text { get; }
        public bool IsCorrect { get; }
    }
}