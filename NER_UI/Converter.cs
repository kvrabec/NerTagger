using System.Drawing;
using System.IO;

namespace NER_UI
{
    public static class Converter
    {
        public static Color ConvertNerTagToColor(NerTagEnum tag)
        {
            switch (tag)
            {
                case NerTagEnum.GeographicalEntity: return Color.Orange;
                case NerTagEnum.Organization: return Color.Red;
                case NerTagEnum.Person: return Color.Blue;
                case NerTagEnum.GeopoliticalEntity: return Color.Aqua;
                case NerTagEnum.DateTime: return Color.Lime;
                case NerTagEnum.Artifact: return Color.DeepPink;
                case NerTagEnum.Event: return Color.DarkViolet;
                case NerTagEnum.NaturalPhenomenon: return Color.DarkGreen;
                default: throw new InvalidDataException($@"Tag ""{tag.ToString()}"" cannot be converted to Color");
            }
        }

        public static NerTagEnum ConvertFromStringToNerTag(string text)
        {
            switch (text)
            {
                case "geo": return NerTagEnum.GeographicalEntity;
                case "org": return NerTagEnum.Organization;
                case "per": return NerTagEnum.Person;
                case "gpe": return NerTagEnum.GeopoliticalEntity;
                case "tim": return NerTagEnum.DateTime;
                case "art": return NerTagEnum.Artifact;
                case "eve": return NerTagEnum.Event;
                case "nat": return NerTagEnum.NaturalPhenomenon;
                default: throw new InvalidDataException($@"Tag ""{text}"" cannot be converted to NerTag");
            }
        }
    }
}