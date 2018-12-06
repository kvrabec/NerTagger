using System.ComponentModel.DataAnnotations;

namespace NER_UI
{
    public enum NerTagEnum
    {
        [Display(Name = "Date and time")]
        DateTime,
        Person,
        Organization,
        [Display(Name = "Geographical entity")]
        GeographicalEntity,
        [Display(Name = "Geopolitical entity")]
        GeopoliticalEntity,
        Artifact,
        Event,
        [Display(Name = "Natural phenomenon")]
        NaturalPhenomenon
    }
}