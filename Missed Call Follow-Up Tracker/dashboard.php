<?php

// Locate the JSON report beside this PHP script
//__DIR__ is similar to Python's script-folder path.
$reportFile = __DIR__ . "/summary.json";

//Stop with a helpful message if Python has not created a report.
if (!is_file($reportFile)) {
    exit("Report not found. Run python3 main.py first.\n");
}

//Read the file's contents as text
$json = file_get_contents($reportFile);

//Reading can fail. === checks both the value and its type
if ($json === false) {
    exit("Could not read the report.\n");
}

try {
    // Convert JSON into a PHP associative array.
    // true lets us access values using their keys
    // JSON_THROW_ON_ERROR raises an exception for invalid JSON
    $summary = json_decode($json, true, 512, JSON_THROW_ON_ERROR);

}catch (JsonException $error) {
    exit("The report contains invalid JSON");
}

// Escape values before placing them into HTML.
// This makes characters such as < display as text.
function escape($value) {
    return htmlspecialchars(
        (string) $value,
        ENT_QUOTES | ENT_SUBSTITUTE,
        "UTF-8"
    );
}

// Read the filter from the URL.
// If none was supplied, show all candidates.
$priorityFilter = $_GET["priority"] ?? "all";

// Accept only the two filter options our page supports.
if (!in_array($priorityFilter, ["all", "High"], true)) {
    $priorityFilter = "all";
}

// Build a list containing only the candidates we want to display.
$visibleCandidates = [];

foreach ($summary["callback_candidates"] as $candidate) {
    if (
        $priorityFilter === "all"
        || $candidate["priority"] === $priorityFilter
    ) {
        $visibleCandidates[] = $candidate;
    }
}
?>



<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="style.css">
    <title>Missed Call Tracker</title>
</head>
<body>
    <h1>Missed Call Tracker</h1>

    <p>
        Report generated:
        <?= escape($summary["generated_at"]) ?>
    </p>

    <h2>Current CSV import</h2>

    <ul>
        <li>Total records: <?= escape($summary["total_calls"]) ?></li>
        <li>Valid calls: <?= escape($summary["valid_call_count"]) ?></li>
        <li>Missed calls: <?= escape($summary["missed_calls"]) ?></li>
        <li>Invalid records: <?= escape($summary["invalid_calls"]) ?></li>
        <li>Duplicate records: <?= escape($summary["duplicate_calls"]) ?></li>
    </ul>

    <h2>Database</h2>

    <p>Total stored calls: <?= escape($summary["stored_calls"]) ?></p>

    <h2>Callback candidates</h2>

    <p>
        High priority starts at
        <?= escape($summary["callback_threshold"]) ?> missed calls.
        These candidates are based on all stored missed calls;
        completed callbacks are not tracked yet.
    </p>
    <!-- GET sends the selected option through the URL -->
    <form method="get">
        <label for="priority">Show callers:</label>

        <select id="priority" name="priority">
            <option value="all"
                <?= $priorityFilter === "all" ? "selected" : "" ?>>
                All Missed Calls
            </option>

            <option value="High"
                <?= $priorityFilter === "High" ? "selected" : "" ?>>
                High priority only
            </option>
        </select>

        <button type="submit">Apply filter</button>
    </form>

    <p>
        Showing <?= count($visibleCandidates) ?> callback candidates.
    </p>

    <table>
        <thead>
            <tr>
                <th scope="col">Phone</th>
                <th scope="col">Missed calls</th>
                <th scope="col">Priority</th>
            </tr>
        </thead>
        <tbody>
            <?php if (count($visibleCandidates) === 0): ?>
                <tr>
                    <td colspan="3">No callers match this filter.</td>
                </tr>
            <?php endif; ?>
            <?php foreach ($visibleCandidates as $candidate): ?>
                   <?php
                            // Choose the appearance based on Python's priority label.
                            // PHP is not recalculating the priority.
                            if ($candidate["priority"] === "High") {
                                $priorityClass = "priority-high";
                            } else {
                                $priorityClass = "priority-normal";
                            }
                    ?>
                <tr>
                    <td><?= escape($candidate["phone"]) ?></td>
                    <td><?= escape($candidate["missed_count"]) ?></td>
                    <td class="<?= escape($priorityClass) ?>">
                        <?= escape($candidate["priority"]) ?>
                    </td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</body>
</html>