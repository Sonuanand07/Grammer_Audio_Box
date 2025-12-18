# 🚀 Kaggle Deployment Guide
## Grammar Scoring Engine from Voice Samples

---

## ⚡ Quick Start

### Option 1: Fastest Way (Recommended)
1. Go to [Kaggle Notebooks](https://www.kaggle.com/notebooks)
2. Create a new notebook
3. Paste the content from `notebooks/grammar_scoring_kaggle.ipynb`
4. Click **Run All**

### Option 2: Upload as Dataset
1. Create a Kaggle dataset with your audio files
2. Link the notebook to your dataset
3. The notebook will automatically process all audio files

---

## 📋 Complete Setup Instructions

### Step 1: Create Kaggle Account
- Go to [kaggle.com](https://www.kaggle.com)
- Sign up with email or Google account
- Verify your email

### Step 2: Prepare Your Audio Files
- Format: WAV, MP3, M4A, or OGG
- Sample rate: 16 kHz recommended
- Duration: 5-120 seconds per file
- Quality: Clear speech (SNR > 20 dB)

### Step 3: Create a Dataset (Optional)
If you want to process multiple audio files:

```bash
# From Kaggle UI:
1. Click "Create" → "Dataset"
2. Upload your audio files
3. Name: "grammar-scoring-audio" (example)
4. Click "Create"
```

### Step 4: Create Notebook
1. Go to Kaggle Notebooks
2. Click "Create" → "Notebook"
3. New Python 3 Notebook
4. In top-right, click "Add input" → Select your dataset
5. Or skip this and use example audio

### Step 5: Copy Code
1. Copy entire content of `notebooks/grammar_scoring_kaggle.ipynb`
2. Paste into Kaggle notebook cells
3. OR: Upload the `.ipynb` file directly

### Step 6: Configure (Optional)
Edit these settings in **Step 2** cell:
```python
ASR_CONFIG = {
    'engine': 'whisper',
    'model_size': 'base',  # or 'tiny', 'small', 'medium', 'large'
    'language': 'en',
}

SCORING_CONFIG = {
    'max_score': 100,
    'weights': {
        'grammar_errors': 0.4,
        'sentence_complexity': 0.3,
        'fluency': 0.2,
        'clarity': 0.1,
    }
}
```

### Step 7: Run Notebook
1. Click **Run All** or run cells individually
2. Wait for dependencies to install (5-10 minutes first run)
3. Watch progress in output
4. View results in **Step 10**

### Step 8: Download Results
- Results saved to `/kaggle/working/`
- Files:
  - `all_results.json` - All scores in JSON
  - `summary.csv` - Tabular format
  - `visualization.png` - Charts
  - `*_results.json` - Individual file results

---

## 🎯 Key Features in Kaggle Notebook

### ✅ Pre-installed
- All required libraries auto-install
- NLTK data auto-downloads
- Whisper model auto-loads

### 🔧 Customizable
- Adjust scoring weights
- Change Whisper model size (base/small/medium)
- Set custom silence threshold

### 📊 Output
- Grammar score (0-100)
- Component breakdown (grammar/fluency/clarity/complexity)
- Detailed error analysis
- Statistical metrics

### ⚙️ Performance
- GPU support (automatic on Kaggle)
- ~2-3 seconds per minute of audio
- Batch processing up to 10 files per run

---

## 🔗 Working with Datasets

### Upload Your Data
```
1. Create dataset in Kaggle
2. Drag-drop audio files
3. Click "Create"
4. Link to notebook: "Add input" → Select dataset
```

### Auto-Detection
The notebook automatically:
- Finds all `.wav`, `.mp3`, `.m4a`, `.ogg` files
- Processes first 10 files (edit limit in Step 9)
- Saves results per file

### Example Data Structure
```
my-dataset/
├── audio_1.wav
├── audio_2.wav
├── audio_3.mp3
└── ...
```

---

## 🐛 Troubleshooting

### Issue: "Module not found" error
**Solution**: Restart kernel and run from top:
1. Click "Kernel" → "Restart kernel"
2. Click "Run All"

### Issue: Out of memory
**Solution**: Reduce Whisper model size:
```python
ASR_CONFIG = {
    'model_size': 'tiny',  # Instead of 'base'
}
```

### Issue: Audio files not found
**Solution**: Check path:
```python
# Verify input location:
for item in os.listdir('/kaggle/input'):
    print(item)
```

### Issue: Whisper download slow
**Solution**: Use smaller model:
```python
'model_size': 'tiny'  # Fastest
'model_size': 'base'  # Balanced (default)
'model_size': 'small' # Better accuracy
```

### Issue: Long audio takes too long
**Solution**: Process less files or increase timeout:
```python
# In Step 9, change:
for i, audio_file in enumerate(audio_files[:5]):  # Only first 5
```

---

## 📊 Output Explanation

### Sample Results
```json
{
  "audio_file": "sample.wav",
  "transcript": "The quick brown fox jumps over the lazy dog",
  "final_score": 85.5,
  "components": {
    "grammar": 90.2,
    "complexity": 78.5,
    "fluency": 82.3,
    "clarity": 88.1
  },
  "errors": {
    "total_errors": 2,
    "error_types": {
      "subject_verb_agreement": 1,
      "article_usage": 1
    }
  },
  "statistics": {
    "total_words": 9,
    "total_sentences": 1,
    "avg_sentence_length": 9.0
  }
}
```

### Component Meanings
- **Grammar** (0-100): Correct grammar usage, no errors
- **Fluency** (0-100): Speech rate, pausing patterns
- **Clarity** (0-100): POS diversity, sentence structure
- **Complexity** (0-100): Sentence length, vocab richness

### Scoring Scale
- **90-100**: Excellent
- **75-89**: Good
- **60-74**: Fair
- **50-59**: Needs improvement
- **<50**: Poor

---

## 🚀 Advanced Usage

### Batch Processing
Process 100s of files:
```python
# Increase limit in Step 9:
for i, audio_file in enumerate(audio_files[:100]):
```

### Custom Weights
Adjust scoring priorities:
```python
SCORING_CONFIG = {
    'weights': {
        'grammar_errors': 0.5,      # More important
        'sentence_complexity': 0.2,
        'fluency': 0.2,
        'clarity': 0.1,
    }
}
```

### Export to Database
Save results to external database:
```python
import requests
# Add custom API call after scoring
requests.post('your-api.com/results', json=result)
```

### Real-time Processing
Stream results:
```python
# Modify score_audio_file() to return real-time updates
```

---

## 📝 Competition/Kaggle Integration

### Publishing Notebook
1. Click "Share" (top right)
2. Select "Notebooks" tab
3. Notebook is now public
4. Add description/tags

### Attracting Upvotes
- Clear documentation ✅
- Reproducible results ✅
- Visualizations ✅
- Error handling ✅
- Comments in code ✅

### Integration with Competitions
- Check Kaggle competitions for relevant challenges
- Modify notebook to match competition requirements
- Submit predictions as required format

---

## 💾 Saving Work

### Create Output Dataset (Share Results)
```python
# Add after Step 11:
import shutil
shutil.make_archive('/kaggle/working/results', 'zip', RESULTS_DIR)
```

Then:
1. Click "Output" (right side)
2. Click "Create new dataset"
3. Select the results folder
4. Publish

### Collaborate
- Share notebook link with others
- Click "Copy and Edit" to fork
- Modifications saved to your copy

---

## 🎓 Learning Resources

### Kaggle Documentation
- [Kaggle Notebooks Guide](https://www.kaggle.com/docs/notebooks)
- [Datasets Help](https://www.kaggle.com/docs/datasets)
- [GPU/TPU Usage](https://www.kaggle.com/docs/kernels)

### Whisper Documentation
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Model Comparisons](https://github.com/openai/whisper#available-models)

### NLTK Resources
- [NLTK Book](https://www.nltk.org/book/)
- [Grammar Patterns](https://www.nltk.org/howto/grammars.html)

---

## ✅ Checklist Before Deployment

- [ ] Audio files in correct format (WAV/MP3/M4A/OGG)
- [ ] Sample rate 16 kHz (auto-converted if needed)
- [ ] Clear speech with minimal background noise
- [ ] Kaggle account created and verified
- [ ] Notebook copied and pasted correctly
- [ ] All cells run without errors
- [ ] Results generate and export correctly
- [ ] Documentation reviewed
- [ ] Ready to share on Kaggle!

---

## 🎯 Next Steps

1. **Deploy Now**
   - Copy notebook to Kaggle
   - Run on your audio files
   - Share results

2. **Improve Accuracy**
   - Use larger Whisper model ('small', 'medium')
   - Add custom grammar rules
   - Tune scoring weights

3. **Scale Up**
   - Create dataset with 100+ audio files
   - Run nightly batch processing
   - Monitor performance metrics

4. **Publish**
   - Make notebook public
   - Add detailed documentation
   - Participate in competitions

---

## 📞 Support

**Issues?** Check:
1. Restart kernel
2. Re-run from top
3. Check file paths
4. Verify audio format
5. Review error messages

**Questions?** 
- Kaggle Community: https://www.kaggle.com/questions-and-answers
- GitHub Issues: [Project Repo]

---

**Happy Grammar Scoring! 🎉**

Created: December 2025 | Status: Production Ready
