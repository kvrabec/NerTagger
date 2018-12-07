using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using Newtonsoft.Json.Linq;
using NER_UI.Model;

namespace NER_UI
{
    public partial class NerTaggerForm : Form
    {
        private readonly string _exeLocation;
        private List<NerEntity> _namedEntities;
        private List<Question> _questions;
        private Question _currentQuestion;
        private string _text;

        public NerTaggerForm()
        {
            // solutionFolder/projectFolder/bin/debug/program.exe
            _exeLocation = Assembly.GetEntryAssembly().Location;
            InitializeComponent();
        }

        private void TagButton_Click(object sender, EventArgs e)
        {
            questionPanel.Visible = false;
            if (textBox.Text == "")
            {
                MessageBox.Show(@"Please enter some text!");
                return;
            }

            using (var loadingForm = new LoadingForm(TagEnteredText))
            {
                loadingForm.StartPosition = FormStartPosition.Manual;
                loadingForm.Location = new Point(Location.X + 250, Location.Y + 200);
                loadingForm.ShowDialog(this);
            }

            FillGridWithNamedEntities();
            GenerateQuestions();
        }

        private void TagEnteredText()
        {
            var pythonApp = Path.GetFullPath(Path.Combine(_exeLocation, @"..\..\..\..\", @"NerTagger\main.py"));

            var pythonProcess = new Process
            {
                StartInfo = new ProcessStartInfo("py.exe")
                {
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    CreateNoWindow = true,
                    Arguments = "-3.5 " + pythonApp + " \"" + textBox.Text.Replace("\"", "\"\"") + "\""
                }
            };

            pythonProcess.Start();
            pythonProcess.ErrorDataReceived += OnErrorDataRecieved;

            var streamReader = pythonProcess.StandardOutput;
            _text = streamReader.ReadToEnd();

            FillNamedEntities(_text);

            pythonProcess.WaitForExit();
            pythonProcess.Close();
        }

        private void OnErrorDataRecieved(object sender, DataReceivedEventArgs e)
        {
            MessageBox.Show(
                $@"Failed to run python script. See error log ""{_exeLocation}/pythonError.log"" for more details.");
            File.WriteAllText(Path.Combine(_exeLocation, "pythonError.log"), e.Data);
        }

        private void FillNamedEntities(string myString)
        {
            _namedEntities = new List<NerEntity>();
            var taggedEntities = new List<string>();
            foreach (var line in myString.Split('\n'))
            {
                var split = line.Split(' ');
                if (split.Length != 2)
                    continue;
                var tag = split[1].Trim();
                if (tag != "O") taggedEntities.Add(line);
            }

            foreach (var entity in taggedEntities)
            {
                var split = entity.Split(' ');
                var word = split[0];
                var nerTag = split[1].Trim();
                var tagSplit = nerTag.Split('-');
                var tagPrefix = tagSplit[0];
                var ner = tagSplit[1];
                if (tagPrefix == "B")
                {
                    _namedEntities.Add(new NerEntity(word, ner));
                }
                else if (tagPrefix == "I")
                {
                    var last = _namedEntities.LastOrDefault();
                    if (last != null && Converter.ConvertFromStringToNerTag(ner) == last.NerTag)
                        last.AppendWordToText(word);
                    else
                        _namedEntities.Add(new NerEntity(word, ner));
                }
            }
        }

        private void FillGridWithNamedEntities()
        {
            if (!_namedEntities.Any())
            {
                richTextBox.SelectedText += "No entites found";
                return;
            }
                
            richTextBox.Text = "";
            var index = 0;
            foreach (var entity in _namedEntities)
            {
                richTextBox.SelectionColor = DefaultForeColor;
                richTextBox.SelectedText += $@"{index++}. {entity.Text} => ";
                richTextBox.SelectionColor = entity.Color;
                richTextBox.SelectionFont = new Font(richTextBox.SelectionFont.Name, 15f, FontStyle.Bold);
                richTextBox.SelectedText += $@"{entity.NerTag}" + Environment.NewLine;
            }
        }

        private void textBox_TextChanged(object sender, EventArgs e)
        {
            if (textBox.Text == "")
                questionPanel.Visible = false;
        }

        private void GenerateQuestions()
        {
            if (!_namedEntities.Any())
                return;
            _questions = new List<Question>();

            if (!questionPanel.Visible && _namedEntities.Any())
                questionPanel.Visible = true;

            var random =new Random();
            var text = "";
            var entity = _namedEntities[random.Next(_namedEntities.Count)];
            foreach (var line in _text.Split('\n'))
            {
                var split = line.Split(' ');
                if (split.Length != 2)
                    continue;
                text += split[0] + " ";
            }

            var sentences = Regex.Split(text, @"(?<=[\.!\?])\s+");

            foreach (var sentence in sentences)
            {
                if (!sentence.Contains(entity.Text))
                    continue;

                var question = sentence.Replace(entity.Text, "__________");
                var answers = GenerateAnswers(entity);
                _questions.Add(new Question(question, answers));

            }

        }

        private HashSet<Answer> GenerateAnswers(NerEntity entity)
        {
            var answers = new HashSet<Answer> {new Answer(entity.Text, true)};
            var random = new Random();
            var filepath = "data/data.json";
            using (var r = new StreamReader(filepath))
            {
                var json = r.ReadToEnd();
                var jobj = JObject.Parse(json);
                while (true)
                {
                    if (answers.Count == 3)
                        break;
                    var answer = jobj[entity.NerTag.ToString()][random.Next(5)].ToString();
                    if (answers.All(ans => ans.Text != answer))
                        answers.Add(new Answer(answer));
                }
            }

            return answers;
        }

        private void NextButton_Click(object sender, EventArgs e)
        {
            _currentQuestion = null;
            if (_questions.Count <= 1 || _questions.All(q => q.isAnswered))
            {
                MessageBox.Show(@"No more questions!");
                return;
            }
                
            _currentQuestion = _questions.First(q => !q.isAnswered);
            questionLabel.Text = _currentQuestion.QuestionText;
            var answers = _currentQuestion.Answers.ToList();
            answerRb1.Text = answers.First().Text;
            answerRb2.Text = answers[1].Text;
            answerRb3.Text = answers.Last().Text;
        }

        private void answerButton_Click(object sender, EventArgs e)
        {
            if(_currentQuestion == null)
            {
                MessageBox.Show(@"You're cheating!!!");
                return;
            }
            var iscorrect = answerRb1.Checked ? CheckAnswer(answerRb1.Text) :
                answerRb2.Checked ? CheckAnswer(answerRb2.Text) :
                CheckAnswer(answerRb3.Text);
            _currentQuestion.isAnswered = true;
            if (iscorrect)
                MessageBox.Show(@"You answered correctly.");
            else
            {
                var correntAnswer = _currentQuestion.Answers.First(ans => ans.IsCorrect);
                MessageBox.Show($@"You answered wrong! Correct answer is {correntAnswer.Text}");
            }
                

        }

        private bool CheckAnswer(string answer)
        {
            return _currentQuestion.Answers.First(ans => ans.Text == answer).IsCorrect;
        }
    }
}