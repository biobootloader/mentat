import * as vscode from "vscode";
import { server } from "./server";
import WebviewProvider from "lib/WebviewProvider";

function getFilepath(args: any[]): string | undefined {
    return (
        args.at(0)?.path ?? vscode.window.activeTextEditor?.document?.fileName
    );
}

export function includeResource(...args: any[]) {
    const filePath = getFilepath(args);
    if (filePath === undefined) {
        return;
    }
    server.sendStreamMessage(filePath, "include");
}

export function excludeResource(...args: any[]) {
    const filePath = getFilepath(args);
    if (filePath === undefined) {
        return;
    }
    server.sendStreamMessage(filePath, "exclude");
}

export function clearChat(...args: any[]) {
    server.sendStreamMessage(null, "clear_conversation");
}

export function eraseChatHistory(
    webviewProvider: WebviewProvider
): (...args: any[]) => void {
    return (...args: any[]) => {
        webviewProvider.sendMessage(null, "vscode:eraseChatHistory");
    };
}
