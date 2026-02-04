import os
from datetime import datetime
from pathlib import Path

class ExtentReport:
  
    def __init__(self, report_name="Test_Execution_Report"):
        self.report_name = report_name
        self.report_dir = "reports"
        self.screenshot_dir = "screenshots"
        self.tests = []
        self.start_time = datetime.now()

        os.makedirs(self.report_dir, exist_ok=True)
        os.makedirs(self.screenshot_dir, exist_ok=True)
        
    def start_test(self, test_name, description=""):
        test_info = {
            'name': test_name,
            'description': description,
            'status': 'RUNNING',
            'start_time': datetime.now(),
            'end_time': None,
            'logs': [],
            'screenshots': [],
            'error': None
        }
        self.tests.append(test_info)
        return test_info
    
    def log(self, test_info, level, message):
        log_entry = {
            'time': datetime.now().strftime('%H:%M:%S'),
            'level': level,
            'message': message
        }
        test_info['logs'].append(log_entry)
    
    def add_screenshot(self, test_info, screenshot_path):
        test_info['screenshots'].append(screenshot_path)
    
    def end_test(self, test_info, status, error=None):
        test_info['status'] = status
        test_info['end_time'] = datetime.now()
        test_info['error'] = error
    
    def generate_report(self):
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        passed = sum(1 for t in self.tests if t['status'] == 'PASS')
        failed = sum(1 for t in self.tests if t['status'] == 'FAIL')
        skipped = sum(1 for t in self.tests if t['status'] == 'SKIP')
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{self.report_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header .info {{ font-size: 14px; opacity: 0.9; }}
        .summary {{ display: flex; justify-content: space-around; padding: 30px; background: white; margin: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat {{ text-align: center; }}
        .stat .number {{ font-size: 36px; font-weight: bold; margin-bottom: 5px; }}
        .stat .label {{ color: #666; font-size: 14px; }}
        .pass {{ color: #10b981; }}
        .fail {{ color: #ef4444; }}
        .skip {{ color: #f59e0b; }}
        .tests {{ margin: 20px; }}
        .test {{ background: white; margin-bottom: 15px; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .test-header {{ padding: 20px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }}
        .test-header:hover {{ background: #f9fafb; }}
        .test-name {{ font-size: 18px; font-weight: 600; }}
        .test-status {{ padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
        .status-pass {{ background: #d1fae5; color: #065f46; }}
        .status-fail {{ background: #fee2e2; color: #991b1b; }}
        .status-skip {{ background: #fef3c7; color: #92400e; }}
        .test-details {{ padding: 20px; background: #f9fafb; border-top: 1px solid #e5e7eb; display: none; }}
        .test-details.active {{ display: block; }}
        .test-description {{ color: #666; margin-bottom: 15px; font-style: italic; }}
        .test-time {{ color: #666; font-size: 13px; margin-bottom: 15px; }}
        .logs {{ margin-top: 15px; }}
        .log-entry {{ padding: 8px 12px; margin: 5px 0; border-radius: 4px; font-size: 13px; font-family: 'Courier New', monospace; }}
        .log-info {{ background: #dbeafe; color: #1e40af; }}
        .log-warning {{ background: #fef3c7; color: #92400e; }}
        .log-error {{ background: #fee2e2; color: #991b1b; }}
        .log-pass {{ background: #d1fae5; color: #065f46; }}
        .error-message {{ background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 4px; margin: 15px 0; border-left: 4px solid #ef4444; }}
        .screenshots {{ margin-top: 15px; }}
        .screenshot {{ margin: 10px 0; }}
        .screenshot img {{ max-width: 100%; border: 1px solid #e5e7eb; border-radius: 4px; cursor: pointer; }}
        .screenshot-title {{ font-weight: 600; margin-bottom: 5px; color: #374151; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 {self.report_name}</h1>
        <div class="info">
            <div>Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}</div>
            <div>End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}</div>
            <div>Duration: {duration:.2f} seconds</div>
        </div>
    </div>
    
    <div class="summary">
        <div class="stat">
            <div class="number">{len(self.tests)}</div>
            <div class="label">Total Tests</div>
        </div>
        <div class="stat">
            <div class="number pass">{passed}</div>
            <div class="label">Passed</div>
        </div>
        <div class="stat">
            <div class="number fail">{failed}</div>
            <div class="label">Failed</div>
        </div>
        <div class="stat">
            <div class="number skip">{skipped}</div>
            <div class="label">Skipped</div>
        </div>
    </div>
    
    <div class="tests">
"""
        
        for idx, test in enumerate(self.tests):
            status_class = test['status'].lower()
            duration_ms = (test['end_time'] - test['start_time']).total_seconds() * 1000 if test['end_time'] else 0
            
            html_content += f"""
        <div class="test">
            <div class="test-header" onclick="toggleDetails({idx})">
                <div class="test-name">{test['name']}</div>
                <span class="test-status status-{status_class}">{test['status']}</span>
            </div>
            <div class="test-details" id="details-{idx}">
                {f'<div class="test-description">{test["description"]}</div>' if test['description'] else ''}
                <div class="test-time">
                    ⏱️ Duration: {duration_ms:.0f}ms | 
                    Started: {test['start_time'].strftime('%H:%M:%S')} | 
                    Ended: {test['end_time'].strftime('%H:%M:%S') if test['end_time'] else 'N/A'}
                </div>
                
                {f'<div class="error-message"><strong>Error:</strong><br>{test["error"]}</div>' if test['error'] else ''}
                
                <div class="logs">
                    <strong>Test Logs:</strong>
"""
            
            for log in test['logs']:
                log_class = f"log-{log['level'].lower()}"
                html_content += f"""
                    <div class="log-entry {log_class}">
                        [{log['time']}] {log['level']}: {log['message']}
                    </div>
"""
            
            html_content += """
                </div>
"""
            
            if test['screenshots']:
                html_content += """
                <div class="screenshots">
                    <strong>Screenshots:</strong>
"""
                for screenshot in test['screenshots']:
                    screenshot_name = os.path.basename(screenshot)
                    html_content += f"""
                    <div class="screenshot">
                        <div class="screenshot-title">📸 {screenshot_name}</div>
                        <img src="../{screenshot}" alt="Screenshot" onclick="window.open(this.src)">
                    </div>
"""
                html_content += """
                </div>
"""
            
            html_content += """
            </div>
        </div>
"""
        
        html_content += """
    </div>
    
    <script>
        function toggleDetails(idx) {
            var details = document.getElementById('details-' + idx);
            details.classList.toggle('active');
        }
    </script>
</body>
</html>
"""
        
        report_filename = f"{self.report_dir}/{self.report_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_filename