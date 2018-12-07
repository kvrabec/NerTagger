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
            this.richTextBox = new System.Windows.Forms.RichTextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.questionPanel = new System.Windows.Forms.Panel();
            this.nextButton = new System.Windows.Forms.Button();
            this.answerButton = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.questionLabel = new System.Windows.Forms.Label();
            this.answerRb3 = new System.Windows.Forms.RadioButton();
            this.answerRb2 = new System.Windows.Forms.RadioButton();
            this.answerRb1 = new System.Windows.Forms.RadioButton();
            this.questionPanel.SuspendLayout();
            this.SuspendLayout();
            // 
            // textBox
            // 
            this.textBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 11F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.textBox.Location = new System.Drawing.Point(80, 29);
            this.textBox.Multiline = true;
            this.textBox.Name = "textBox";
            this.textBox.Size = new System.Drawing.Size(607, 150);
            this.textBox.TabIndex = 0;
            this.textBox.TextChanged += new System.EventHandler(this.textBox_TextChanged);
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
            this.tagButton.Location = new System.Drawing.Point(693, 31);
            this.tagButton.Name = "tagButton";
            this.tagButton.Size = new System.Drawing.Size(83, 23);
            this.tagButton.TabIndex = 2;
            this.tagButton.Text = "Tag";
            this.tagButton.UseVisualStyleBackColor = true;
            this.tagButton.Click += new System.EventHandler(this.TagButton_Click);
            // 
            // richTextBox
            // 
            this.richTextBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 15F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.richTextBox.Location = new System.Drawing.Point(80, 192);
            this.richTextBox.Name = "richTextBox";
            this.richTextBox.Size = new System.Drawing.Size(607, 150);
            this.richTextBox.TabIndex = 7;
            this.richTextBox.Text = "";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(33, 185);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(41, 13);
            this.label3.TabIndex = 8;
            this.label3.Text = "Entities";
            // 
            // questionPanel
            // 
            this.questionPanel.Controls.Add(this.nextButton);
            this.questionPanel.Controls.Add(this.answerButton);
            this.questionPanel.Controls.Add(this.label2);
            this.questionPanel.Controls.Add(this.questionLabel);
            this.questionPanel.Controls.Add(this.answerRb3);
            this.questionPanel.Controls.Add(this.answerRb2);
            this.questionPanel.Controls.Add(this.answerRb1);
            this.questionPanel.Location = new System.Drawing.Point(28, 348);
            this.questionPanel.Name = "questionPanel";
            this.questionPanel.Size = new System.Drawing.Size(659, 138);
            this.questionPanel.TabIndex = 10;
            this.questionPanel.Visible = false;
            // 
            // nextButton
            // 
            this.nextButton.Location = new System.Drawing.Point(550, 100);
            this.nextButton.Name = "nextButton";
            this.nextButton.Size = new System.Drawing.Size(75, 23);
            this.nextButton.TabIndex = 13;
            this.nextButton.Text = "Next";
            this.nextButton.UseVisualStyleBackColor = true;
            this.nextButton.Click += new System.EventHandler(this.NextButton_Click);
            // 
            // answerButton
            // 
            this.answerButton.Location = new System.Drawing.Point(460, 100);
            this.answerButton.Name = "answerButton";
            this.answerButton.Size = new System.Drawing.Size(75, 23);
            this.answerButton.TabIndex = 12;
            this.answerButton.Text = "Answer";
            this.answerButton.UseVisualStyleBackColor = true;
            this.answerButton.Click += new System.EventHandler(this.answerButton_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(5, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(49, 13);
            this.label2.TabIndex = 11;
            this.label2.Text = "Question";
            // 
            // questionLabel
            // 
            this.questionLabel.AutoSize = true;
            this.questionLabel.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(238)));
            this.questionLabel.Location = new System.Drawing.Point(66, 14);
            this.questionLabel.Name = "questionLabel";
            this.questionLabel.Size = new System.Drawing.Size(0, 20);
            this.questionLabel.TabIndex = 3;
            // 
            // answerRb3
            // 
            this.answerRb3.AutoSize = true;
            this.answerRb3.Location = new System.Drawing.Point(52, 105);
            this.answerRb3.Name = "answerRb3";
            this.answerRb3.Size = new System.Drawing.Size(14, 13);
            this.answerRb3.TabIndex = 2;
            this.answerRb3.TabStop = true;
            this.answerRb3.UseVisualStyleBackColor = true;
            // 
            // answerRb2
            // 
            this.answerRb2.AutoSize = true;
            this.answerRb2.Location = new System.Drawing.Point(52, 85);
            this.answerRb2.Name = "answerRb2";
            this.answerRb2.Size = new System.Drawing.Size(14, 13);
            this.answerRb2.TabIndex = 1;
            this.answerRb2.TabStop = true;
            this.answerRb2.UseVisualStyleBackColor = true;
            // 
            // answerRb1
            // 
            this.answerRb1.AutoSize = true;
            this.answerRb1.Location = new System.Drawing.Point(52, 66);
            this.answerRb1.Name = "answerRb1";
            this.answerRb1.Size = new System.Drawing.Size(14, 13);
            this.answerRb1.TabIndex = 0;
            this.answerRb1.TabStop = true;
            this.answerRb1.UseVisualStyleBackColor = true;
            // 
            // NerTaggerForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(784, 511);
            this.Controls.Add(this.questionPanel);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.richTextBox);
            this.Controls.Add(this.tagButton);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.textBox);
            this.Name = "NerTaggerForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "NER Tagger";
            this.questionPanel.ResumeLayout(false);
            this.questionPanel.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox textBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button tagButton;
        private System.Windows.Forms.RichTextBox richTextBox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Panel questionPanel;
        private System.Windows.Forms.Label questionLabel;
        private System.Windows.Forms.RadioButton answerRb3;
        private System.Windows.Forms.RadioButton answerRb2;
        private System.Windows.Forms.RadioButton answerRb1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button nextButton;
        private System.Windows.Forms.Button answerButton;
    }
}

