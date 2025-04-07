from burp import IBurpExtender, IContextMenuFactory
from javax.swing import JMenuItem, JOptionPane, JPanel, JLabel, JTextField, BoxLayout, JFileChooser, JRadioButton, ButtonGroup, JCheckBox
from java.awt.event import ItemListener
from java.awt import Toolkit, datatransfer
import re
import os
import time

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self.callbacks = callbacks
        self.helpers = callbacks.getHelpers()
        callbacks.setExtensionName("GAL (Get All URLs)")

        callbacks.registerContextMenuFactory(self)
        callbacks.printOutput("[+] GAL extension loaded.")

    def createMenuItems(self, invocation):
        self.invocation = invocation
        return [JMenuItem("Extract URLs by file type or regex", actionPerformed=self.extract_urls)]

    def extract_urls(self, event):
        panel = JPanel()
        panel.setLayout(BoxLayout(panel, BoxLayout.Y_AXIS))

        ext_radio = JRadioButton("Match by extension", True)
        regex_radio = JRadioButton("Use full regex pattern", False)
        group = ButtonGroup()
        group.add(ext_radio)
        group.add(regex_radio)

        ext_field = JTextField("js")
        regex_field = JTextField(".*")
        regex_field.setEnabled(False)

        split_checkbox = JCheckBox("Split output into separate domain folders", False)
        clipboard_checkbox = JCheckBox("Copy results to clipboard", False)

        class ToggleListener(ItemListener):
            def itemStateChanged(self, event):
                ext_field.setEnabled(ext_radio.isSelected())
                regex_field.setEnabled(regex_radio.isSelected())

        toggle_listener = ToggleListener()
        ext_radio.addItemListener(toggle_listener)
        regex_radio.addItemListener(toggle_listener)

        panel.add(ext_radio)
        panel.add(ext_field)
        panel.add(regex_radio)
        panel.add(regex_field)
        panel.add(split_checkbox)
        panel.add(clipboard_checkbox)

        result = JOptionPane.showConfirmDialog(None, panel, "Input", JOptionPane.OK_CANCEL_OPTION)
        if result != JOptionPane.OK_OPTION:
            return

        selected_messages = self.invocation.getSelectedMessages()
        if not selected_messages:
            JOptionPane.showMessageDialog(None, "Please select at least one item from the Site map.")
            return

        selected_hosts = {self.helpers.analyzeRequest(msg).getUrl().getHost() for msg in selected_messages}
        site_map = self.callbacks.getSiteMap(None)

        matched_by_host = {}

        if ext_radio.isSelected():
            file_types = [ft.strip().lstrip('.') for ft in ext_field.getText().split(',') if ft.strip()]
            pattern = re.compile(r'\.(' + '|'.join(map(re.escape, file_types)) + r')(?:$|\?)', re.IGNORECASE)
        else:
            regex_filter = regex_field.getText().strip()
            try:
                pattern = re.compile(regex_filter, re.IGNORECASE)
            except:
                JOptionPane.showMessageDialog(None, "Invalid regex pattern.")
                return

        for item in site_map:
            url = item.getUrl().toString()
            host = item.getUrl().getHost()
            if host in selected_hosts and pattern.search(url):
                if host not in matched_by_host:
                    matched_by_host[host] = set()
                matched_by_host[host].add(url)

        if not matched_by_host:
            JOptionPane.showMessageDialog(None, "No matching URLs found.")
            return

        chooser = JFileChooser()
        chooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
        chooser.setDialogTitle("Select directory to save extracted URLs")
        ret = chooser.showSaveDialog(None)

        if ret != JFileChooser.APPROVE_OPTION:
            JOptionPane.showMessageDialog(None, "No directory selected. Aborting.")
            return

        base_dir = chooser.getSelectedFile().getAbsolutePath()
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        total_urls = 0
        all_collected_urls = []

        if split_checkbox.isSelected():
            for host, urls in matched_by_host.items():
                host_dir = os.path.join(base_dir, host)
                if not os.path.exists(host_dir):
                    os.makedirs(host_dir)
                filename = "extracted_urls_{}.txt".format(timestamp)
                path = os.path.join(host_dir, filename)
                with open(path, 'w') as f:
                    f.write("\n".join(sorted(urls)))
                all_collected_urls.extend(sorted(urls))
                total_urls += len(urls)
                self.callbacks.printOutput("[+] Saved {} URLs for {} -> {}".format(len(urls), host, path))
        else:
            all_urls = set()
            for urls in matched_by_host.values():
                all_urls.update(urls)
            filename = "extracted_urls_{}.txt".format(timestamp)
            path = os.path.join(base_dir, filename)
            with open(path, 'w') as f:
                f.write("\n".join(sorted(all_urls)))
            all_collected_urls = sorted(all_urls)
            total_urls = len(all_urls)
            self.callbacks.printOutput("[+] Saved all {} URLs -> {}".format(total_urls, path))

        if clipboard_checkbox.isSelected():
            clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
            clipboard.setContents(datatransfer.StringSelection("\n".join(all_collected_urls)), None)

        JOptionPane.showMessageDialog(None, "{} URLs extracted and saved successfully.{}".format(
            total_urls,
            "\n(Results copied to clipboard)" if clipboard_checkbox.isSelected() else ""))
