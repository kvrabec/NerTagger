using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Windows.Forms;

namespace NER_UI
{
    public partial class NerTaggerForm : Form
    {
        private readonly string _exeLocation;
        private List<NerEntity> _namedEntities;
        private string _processOutput;

        public NerTaggerForm()
        {
            // solutionFolder/projectFolder/bin/debug/program.exe
            _exeLocation = Assembly.GetEntryAssembly().Location;
            InitializeComponent();
        }

        private void TagButton_Click(object sender, EventArgs e)
        {
            if (textBox.Text == "")
            {
                MessageBox.Show(@"Please enter some text!");
                return;
            }

            _processOutput = "";

            using (var loadingForm = new LoadingForm(TagEnteredText))
            {
                loadingForm.StartPosition = FormStartPosition.Manual;
                loadingForm.Location = new Point(Location.X + 250, Location.Y + 200);
                loadingForm.ShowDialog(this);
            }

            taggedTextBox.Text = ProcessString(_processOutput);
            FillGridWithNamedEntities();
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
                    Arguments = "-3.5 " + pythonApp + " \"" + textBox.Text + "\""
                }
            };

            pythonProcess.Start();
            pythonProcess.ErrorDataReceived += OnErrorDataRecieved;

            var streamReader = pythonProcess.StandardOutput;
            _processOutput = streamReader.ReadToEnd();

            pythonProcess.WaitForExit();
            pythonProcess.Close();
        }

        private void OnErrorDataRecieved(object sender, DataReceivedEventArgs e)
        {
            MessageBox.Show(
                $@"Failed to run python script. See error log ""{_exeLocation}/pythonError.log"" for more details.");
            File.WriteAllText(Path.Combine(_exeLocation, "pythonError.log"), e.Data);
        }

        private string ProcessString(string myString)
        {
            _namedEntities = new List<NerEntity>();
            var output = string.Empty;
            var taggedEntities = new List<string>();
            foreach (var line in myString.Split('\n'))
            {
                var split = line.Split(' ');
                var word = split[0];
                if (split.Length != 2)
                    continue;
                output += word + " ";
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
                    var last = _namedEntities.Last();
                    if (Converter.ConvertFromStringToNerTag(ner) == last.NerTag)
                        last.AppendWordToText(word);
                    else
                        _namedEntities.Add(new NerEntity(word, ner));
                }
            }

            var index = 1;
            foreach (var entity in _namedEntities)
                output = output.Replace(entity.Text, entity.GetFormatedText(index++));

            return output.Trim();
        }

        private void FillGridWithNamedEntities()
        {
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
    }
}