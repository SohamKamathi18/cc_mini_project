# 🔧 Quick Troubleshooting Guide

## Issue: Preview Still Blank After Fix

### Step 1: Check Console (F12)
Look for these logs in order:

```javascript
✅ "Submitting form:" {business_name: "...", ...}
✅ "API Response:" {success: true, html: "...", ...}
✅ "ResultPreview data:" {success: true, html: "...", ...}
```

**If you DON'T see these logs:**
- Frontend might not have reloaded
- Try: Stop frontend (Ctrl+C) and run `npm run dev` again

---

## Issue: "Failed to generate website"

### Check Backend Terminal
Look for error messages like:

```
❌ Error generating website: ...
```

**Common Causes:**
1. **Missing API Key**: Check `.env` file has `GOOGLE_API_KEY`
2. **Agents Not Initialized**: Backend should show "Agents initialized" on startup
3. **Template Error**: Check if template files exist

**Fix:**
```bash
# Check .env file
cat .env  # or type .env in PowerShell

# Should contain:
GOOGLE_API_KEY=your_actual_key_here
UNSPLASH_ACCESS_KEY=your_key_here

# Restart backend
python api.py
```

---

## Issue: Iframe Shows Nothing

### Possible Causes:

#### 1. HTML is Empty or Invalid
Check console log:
```javascript
console.log('HTML length:', data.html?.length)
```

If length is 0 or undefined → Backend didn't generate HTML

**Fix:** Check backend logs for HTML generation errors

#### 2. Iframe Security Blocked
Check console for errors like:
```
Blocked frame with origin ...
```

**Fix:** Already added to iframe:
```javascript
sandbox="allow-scripts allow-same-origin allow-popups"
```

#### 3. HTML Has Errors
Try "Open in New Tab" button to see if HTML works outside iframe

---

## Issue: Design/Content Details Missing

### Check Data Structure
In console, look at the logged data:

```javascript
// Good structure
{
  design: { primary_color: "#xxx", ... },
  content: { hero_headline: "...", ... }
}

// Bad structure (old format)
{
  design: "some string",  // ❌ Should be object
  content: "some string"  // ❌ Should be object
}
```

**If structure is wrong:**
- Backend might be returning old format
- Check `api.py` line ~200 for return structure

---

## Issue: Animation Completes But No Preview

### Check Network Tab
1. Open DevTools (F12)
2. Go to Network tab
3. Submit form
4. Look for POST to `/api/generate`

**What to check:**
- Status: Should be `200 OK`
- Response: Should have `success: true` and `html` field
- Time: Should complete within 30 seconds

**If Status is 500:**
- Backend error
- Check backend terminal for details

**If Status is 404:**
- API endpoint not found
- Check backend is running on port 5000

**If Request is Pending forever:**
- Backend might be stuck
- Restart backend
- Check API key is valid

---

## Issue: "ECONNREFUSED" Error

### This means frontend can't reach backend

**Check:**
1. Is backend running? Should see:
   ```
   API running on: http://localhost:5000
   ```

2. Is it on correct port?
   ```bash
   # Should show python process on port 5000
   netstat -ano | findstr :5000
   ```

3. Is proxy configured correctly?
   Check `frontend/vite.config.js`:
   ```javascript
   target: 'http://127.0.0.1:5000',  // Must be 127.0.0.1, not localhost
   ```

**Fix:**
```bash
# Restart backend
python api.py

# Restart frontend
cd frontend
npm run dev
```

---

## Issue: Form Doesn't Submit

### Check Validation
All fields must be filled:
- ✅ Business Name (min 2 chars)
- ✅ Description (min 20 chars)
- ✅ Services
- ✅ Target Audience
- ✅ Color Preference
- ✅ Style Preference

**Red borders around fields?**
- Fill them properly
- Check character minimums

---

## Issue: Download Button Doesn't Work

### Check Browser Settings
- Pop-up blocker might be blocking download
- Check if download started in browser's download bar

### Try Alternative:
Click "Open in New Tab" then use browser's Save Page As

---

## Complete Reset (Nuclear Option)

If nothing works, do a complete reset:

```bash
# 1. Stop all terminals (Ctrl+C in each)

# 2. Restart backend
python api.py

# Wait for: "✅ All agents initialized"

# 3. In new terminal, restart frontend
cd frontend
npm run dev

# 4. Open fresh browser tab
# Go to: http://localhost:3000

# 5. Open DevTools (F12)
# Watch console while testing

# 6. Fill form and submit
# Watch for the three console logs
```

---

## Still Not Working?

### Gather Debug Info:

1. **Console Logs:**
   - Take screenshot of console (F12)
   - Look for red error messages

2. **Network Tab:**
   - Screenshot of `/api/generate` request
   - Show status code and response

3. **Backend Logs:**
   - Copy last 50 lines from backend terminal

4. **Data Structure:**
   - Copy the logged `data` object from console

### Create a Test Case:

```javascript
// In browser console, paste this:
fetch('/api/health')
  .then(r => r.json())
  .then(d => console.log('Health check:', d))
  .catch(e => console.error('Health check failed:', e))

// Should output:
// Health check: {status: "ok", message: "API is running", agents_initialized: true}
```

If health check fails → Backend connection issue
If health check works but generate fails → Backend processing issue

---

## Common Success Path

✅ Fill all form fields
✅ Click "Generate My Website"
✅ See animation for ~12 seconds
✅ See "Your Website is Ready! 🎉"
✅ Preview loads in browser frame
✅ See design colors and details
✅ Download button creates HTML file

**Timeline: ~12-15 seconds from submit to preview**

---

## Performance Issues

### If API takes too long (>30 seconds):

1. **Check API Key Quota:**
   - Google Gemini might be rate-limited
   - Check Gemini dashboard

2. **Simplify Request:**
   - Use shorter descriptions
   - Fewer services

3. **Check Network:**
   - Slow internet affects Gemini API
   - Unsplash image fetching

---

## Browser Compatibility

**Tested & Working:**
- ✅ Chrome/Edge (Latest)
- ✅ Firefox (Latest)
- ✅ Safari (Latest)

**Known Issues:**
- ⚠️ Old browsers might not support `srcDoc` attribute
- ⚠️ IE11 not supported (no modern JS)

---

**If you're still stuck, check the console logs and compare with the expected output in BUG_FIX_SUMMARY.md!** 🔍
