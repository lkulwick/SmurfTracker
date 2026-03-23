#include "pch.h"
#include "SmurfTracker.h"

void SmurfTracker::RenderSettings() {
    ImGui::TextUnformatted("General Settings");

    // Enable Render Checkbox
    CVarWrapper enableCvar = cvarManager->getCvar("SmurfTracker_enabled");
    if (!enableCvar) { return; }
    bool enabled = enableCvar.getBoolValue();
    if (ImGui::Checkbox("Enable plugin", &enabled)) {
        enableCvar.setValue(enabled);
    }
    if (ImGui::IsItemHovered()) {
        ImGui::SetTooltip("Toggle SmurfTracker Plugin");
    }

    // Mode Combo Box
    CVarWrapper modeCvar = cvarManager->getCvar("SmurfTracker_mode");
    if (!modeCvar) { return; } 
    int selectedMode = modeCvar.getIntValue();
    const char* items[] = { "Score", "MMR", "Wins" }; // Modes
    if (ImGui::Combo("Mode", &selectedMode, items, IM_ARRAYSIZE(items))) {
        modeCvar.setValue(selectedMode);
    }
    if (ImGui::IsItemHovered()) { 
        ImGui::SetTooltip("Select the mode to display"); 
    }

    ImGui::Separator();
    ImGui::TextUnformatted("Wins mode settings:");
    ImGui::TextWrapped("Wins are fetched directly from RLStats. No local shim or Docker container is required.");

    ImGui::TextUnformatted("Does not work yet:");
    CVarWrapper checkTeammatesCvar = cvarManager->getCvar("SmurfTracker_check_teammates");
    if (!checkTeammatesCvar) { return; }
    bool checkTeammates = checkTeammatesCvar.getBoolValue();
    if (ImGui::Checkbox("Check teammates", &checkTeammates)) {
        checkTeammatesCvar.setValue(checkTeammates);
    }
    if (ImGui::IsItemHovered()) {
        ImGui::SetTooltip("Disable checking teammates stats to reduce API calls");
    }

    CVarWrapper checkSelfCvar = cvarManager->getCvar("SmurfTracker_check_self");
    if (!checkSelfCvar) { return; }
    bool checkSelf = checkSelfCvar.getBoolValue();
    if (ImGui::Checkbox("Check yourself", &checkSelf)) {
        checkSelfCvar.setValue(checkSelf);
    }
    if (ImGui::IsItemHovered()) {
        ImGui::SetTooltip("Disable checking your own stats to reduce API calls");
    }
    ImGui::Separator();
}
