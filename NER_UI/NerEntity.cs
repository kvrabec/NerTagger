using System.Drawing;

namespace NER_UI
{
    public class NerEntity
    {
        public NerEntity(string word, string tag)
        {
            NerTag = Converter.ConvertFromStringToNerTag(tag);
            Text = word;
            Color = Converter.ConvertNerTagToColor(NerTag);
        }

        public string Text { get; private set; }
        public NerTagEnum NerTag { get; }
        public Color Color { get; }

        public void AppendWordToText(string word)
        {
            Text += $@" {word}";
        }

        public string GetFormatedText(int index)
        {
            return $@"({index}. {Text})";
        }
    }
}