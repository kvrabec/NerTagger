using System;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace NER_UI
{
    public partial class LoadingForm : Form
    {

        public Action Worker { get; set; }
        public LoadingForm(Action worker)
        {
            InitializeComponent();
            Worker = worker ?? throw new ArgumentNullException();
        }

        protected override void OnLoad(EventArgs e)
        {
            Task.Factory.StartNew(Worker)
                .ContinueWith(t => { Close(); }, TaskScheduler.FromCurrentSynchronizationContext());
        }
    }
}