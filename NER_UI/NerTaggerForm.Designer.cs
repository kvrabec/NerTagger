namespace NER_UI
{
    partial class NerTaggerForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.textBox = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.tagButton = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.richTextBox = new System.Windows.Forms.RichTextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.taggedTextBox = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // textBox
            // 
            this.textBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 11F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.textBox.Location = new System.Drawing.Point(80, 29);
            this.textBox.Multiline = true;
            this.textBox.Name = "textBox";
            this.textBox.Size = new System.Drawing.Size(600, 150);
            this.textBox.TabIndex = 0;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(46, 29);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(28, 13);
            this.label1.TabIndex = 1;
            this.label1.Text = "Text";
            // 
            // tagButton
            // 
            this.tagButton.Location = new System.Drawing.Point(701, 36);
            this.tagButton.Name = "tagButton";
            this.tagButton.Size = new System.Drawing.Size(75, 23);
            this.tagButton.TabIndex = 2;
            this.tagButton.Text = "Tag";
            this.tagButton.UseVisualStyleBackColor = true;
            this.tagButton.Click += new System.EventHandler(this.TagButton_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 202);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(64, 13);
            this.label2.TabIndex = 4;
            this.label2.Text = "Tagged text";
            // 
            // richTextBox
            // 
            this.richTextBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.richTextBox.Location = new System.Drawing.Point(80, 339);
            this.richTextBox.Name = "richTextBox";
            this.richTextBox.Size = new System.Drawing.Size(600, 150);
            this.richTextBox.TabIndex = 7;
            this.richTextBox.Text = "";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(35, 339);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(41, 13);
            this.label3.TabIndex = 8;
            this.label3.Text = "Entities";
            // 
            // taggedTextBox
            // 
            this.taggedTextBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 11F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.taggedTextBox.Location = new System.Drawing.Point(80, 185);
            this.taggedTextBox.Multiline = true;
            this.taggedTextBox.Name = "taggedTextBox";
            this.taggedTextBox.ReadOnly = true;
            this.taggedTextBox.Size = new System.Drawing.Size(600, 150);
            this.taggedTextBox.TabIndex = 9;
            // 
            // NerTaggerForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(784, 511);
            this.Controls.Add(this.taggedTextBox);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.richTextBox);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.tagButton);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.textBox);
            this.Name = "NerTaggerForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "NER Tagger";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button tagButton;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.RichTextBox richTextBox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox taggedTextBox;
    }
}

